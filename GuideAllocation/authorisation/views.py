from django.shortcuts import render
import pyrebase
import random
from django.core.mail import send_mail
import firebase_admin
from firebase_admin import credentials, auth, db
from django.http import JsonResponse

# Firebase Configuration
config = {
    "apiKey": "AIzaSyCfq_OuJ2sHNPFjV_tFsJzUp3cQbD8-M3E",
    "authDomain": "mtech-project-authentication.firebaseapp.com",
    "databaseURL": "https://mtech-project-authentication-default-rtdb.firebaseio.com",
    "projectId": "mtech-project-authentication",
    "storageBucket": "mtech-project-authentication.appspot.com",
    "messagingSenderId": "160353375587",
    "appId": "1:160353375587:web:57f5c18539f2807d2def56"
}

# Initialising pyrebase for authentication
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()

# Initialize Firebase Admin SDK (for Database)
cred = credentials.Certificate("mtech-project-authentication-firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {'databaseURL': config['databaseURL']})

# Get reference to the Firebase database
database = db.reference()

# Send OTP using Firebase's phone authentication
def send_otp(request):
    phone_number = request.POST.get('phone')

    try:
        # Send verification code to the phone number (mock)
        verification = auth.create_session_cookie(phone_number, expires_in=60 * 5)
        request.session['verification'] = verification
        return JsonResponse({"status": "success", "message": "OTP sent successfully."})
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return JsonResponse({"status": "error", "message": f"Failed to send OTP: {e}"})

# Verify the OTP
def verify_phone_otp(request):
    otp = request.POST.get('otp')
    session_verification = request.session.get('verification')

    try:
        if session_verification and otp == session_verification:
            return JsonResponse({"status": "success", "message": "OTP verified successfully!"})
        else:
            return JsonResponse({"status": "error", "message": "Invalid OTP."})
    except Exception as e:
        print(f"Error verifying OTP: {e}")
        return JsonResponse({"status": "error", "message": "Failed to verify OTP."})

def signIn(request):
    return render(request, "Login.html")

def home(request):
    return render(request, "Home.html")

def postsignIn(request):
    email = request.POST.get('email')
    pasw = request.POST.get('pass')
    try:
        user = authe.sign_in_with_email_and_password(email, pasw)
        request.session['uid'] = user['idToken']
        return render(request, "Home.html", {"email": email})
    except Exception as e:
        print(f"Error during sign-in: {e}")
        message = "Invalid Credentials! Please check your data."
        return render(request, "Login.html", {"message": message})

def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request, "Login.html")

def signUp(request):
    return render(request, "Registration.html")

def postsignUp(request):
    email = request.POST.get('email')
    password = request.POST.get('pass')
    name = request.POST.get('name')
    idn = request.POST.get('id')
    phone = request.POST.get('phone')
    is_professor = request.POST.get('isProfessor') == 'on'
    is_admin = request.POST.get('isAdmin') == 'on'

    try:
        # Validation checks
        if len(phone) != 14:
            raise ValueError("Phone number must be 10 digits long.")
        
        if is_professor:
            if not idn.strip():
                raise ValueError("Professor ID cannot be empty.")
        else:
            if len(idn) != 8:
                raise ValueError("Roll number must be 8 characters long.")
        
        if is_admin and not is_professor:
            raise ValueError("Only professors can be admins.")

        # Creating a user with the given email and password
        user = authe.create_user_with_email_and_password(email, password)
        uid = user['localId']

        # Log success of user creation
        print(f"User created with UID: {uid}")

        # Set uid in session
        request.session['uid'] = uid

        # Prepare user data for database
        user_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "is_professor": is_professor,
            "is_admin": is_admin,
            "password": password,
            "idn": idn
        }

        # Writing user details to the Firebase Realtime Database
        database.child("users").child(uid).set(user_data)
        print(f"User data written to database for UID: {uid}")

        # Redirect to Home.html after successful signup
        return render(request, "Home.html")

    except ValueError as e:
        return render(request, "Registration.html", {"error_message": str(e)})
    except Exception as e:
        print(f"Error during signup: {e}")
        return render(request, "Registration.html", {"error_message": "An error occurred during signup. Please try again."})

def reset(request):
    return render(request, "Reset.html")

def postReset(request):
    email = request.POST.get('email')
    try:
        authe.send_password_reset_email(email)
        message = "A reset password email has been sent successfully."
        return render(request, "Reset.html", {"msg": message})
    except Exception as e:
        print(f"Error sending reset email: {e}")
        message = "Something went wrong, please check if the email is registered."
        return render(request, "Reset.html", {"msg": message})

# POST OTP Function
def postOtp(request):
    email = request.POST.get('email')
    password = request.POST.get('pass')

    # Initialize user_data and uid
    user_data = None
    uid = request.session.get('uid')

    try:
        # Authenticate the user using Firebase Authentication
        user = authe.sign_in_with_email_and_password(email, password)
        uid = user['localId']  # Store the user's unique ID (localId)
        request.session['uid'] = uid  # Store the UID in the session

        # Fetch data from Firebase where roll_no (idn) is the key after user is authenticated
        # user_data = database.child("users").child(uid).get().val()
        user_data = database.child("users").child(uid).get()
        if not user_data:
            raise ValueError("User data not found in the database.")
        
        # Validate roll number (idn) for IT department
        idn = user_data.get("idn")
        if idn and len(idn) >= 5:
            if idn[3:5] != "IT":
                message = "Invalid Roll no! Only IT roll numbers are allowed."
                return render(request, "Login.html", {"message": message})
        else:
            message = "Invalid Roll no! Please check your data."
            return render(request, "Login.html", {"message": message})

    except Exception as e:
        print(f"Error during authentication: {e}")
        message = "Invalid Credentials! Please check your email and password."
        return render(request, "Login.html", {"message": message})

    # OTP generation and email sending logic
    try:
        otp = random.randint(100000, 999999)

        # Save OTP and email in session for verification
        request.session['otp'] = otp
        request.session['email'] = email

        # Send OTP via email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            'tanvi.poddar123@gmail.com',  # Sender's email
            [email],  # Recipient's email
            fail_silently=False,
        )

        # Success message for OTP email
        message = "An email with an OTP for verification has been sent."
        return render(request, "otp.html", {"msg": message, "email": email})

    except Exception as e:
        print(f"Error during OTP sending: {e}")
        message = f"Something went wrong while sending OTP to {email}. Error: {e}"
        return render(request, "otp.html", {"msg": message})

# Function to verify OTP
def verify_otp(request):
    user_otp = request.POST.get('otp')
    session_otp = request.session.get('otp')
    email = request.session.get('email')

    if int(user_otp) == session_otp:  # OTP matches
        message = "OTP verified successfully!"
        return render(request, "Home.html", {"msg": message, "email": email})
    else:
        message = "Invalid OTP. Please try again."
        return render(request, "otp.html", {"msg": message, "email": email})

def profile(request):
    try:
        uid = request.session.get('uid')
        if uid:
            user_data = database.child("users").child(uid).get().val()
            if not user_data:
                return render(request, "profile.html", {"msg": "No user data found."})

            name = user_data.get("name")
            email = user_data.get("email")

            context = {
                "name": name,
                "email": email,
            }
            return render(request, "profile.html", context)
        else:
            return render(request, "Login.html", {"message": "You need to log in first."})
    except Exception as e:
        print(f"Error fetching profile data: {e}")
        return render(request, "profile.html", {"msg": "Error fetching profile data."})

def update_profile(request):
    if request.method == 'POST':
        uid = request.session.get('uid')
        if uid:
            name = request.POST.get('name')
            phone = request.POST.get('phone')

            try:
                # Update user data in Firebase
                database.child("users").child(uid).update({
                    "name": name,
                    "phone": phone,
                })
                message = "Profile updated successfully!"
                return render(request, "profile.html", {"msg": message})
            except Exception as e:
                print(f"Error updating profile: {e}")
                return render(request, "profile.html", {"msg": "Error updating profile."})
        else:
            return render(request, "Login.html", {"message": "You need to log in first."})

    # If request method is GET, show the profile page
    return profile(request)
def emailver(request):
    email = request.POST.get('email')
    password = request.POST.get('pass')

    # Get uid from the session (could be None if user is not signed in yet)
    uid = request.session.get('uid')
    
    # Initialize an empty user_data variable
    user_data = None
    try:
        # Generate a 6-digit OTP
        otp = random.randint(100000, 999999)

        # Save OTP and email in session for later verification
        request.session['otp'] = otp
        request.session['email'] = email

        # Send the OTP to the provided email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            'tanvi.poddar123@gmail.com',  # Sender's email
            [email],  # Recipient's email
            fail_silently=False,  # Raise exceptions if something goes wrong
        )

        # Success message for OTP email
        message = "An email with an OTP for verification has been sent."
        return render(request, "emailveri.html", {"msg": message, "email": email})

    except Exception as e:
        # Print detailed error message and return an error page
        print(f"Error during OTP sending: {e}")
        message = f"Something went wrong while sending OTP to {email}. Error: {e}"
        return render(request, "emailveri.html", {"msg": message})

