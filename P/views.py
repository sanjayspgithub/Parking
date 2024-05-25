from django.shortcuts import render, redirect
from .models import Visitor, Userlogin, park_vehicle
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
import threading
import cv2
import base64
import os
from datetime import datetime
import pytesseract
from django.http import JsonResponse
from django.db import connection

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

def process_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(25, 25))

    plate_texts = []
    image_name = ''
    for idx, (x, y, w, h) in enumerate(plates):
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        plate_region = image[y:y + h, x:x + w]
        plate_gray = cv2.cvtColor(plate_region, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(plate_gray, config='--psm 8')
        plate_texts.append(text.strip())
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        image_name = str(timestamp) + '_cropped.jpg'
        cropped_image_path = f'static/vehicletrace/'+image_name
        cv2.imwrite(cropped_image_path, plate_region)

    return image, plate_texts, image_name


def video_feed(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data', '')
        if image_data.startswith('data:image/jpeg;base64,'):
            image_data = image_data.replace('data:image/jpeg;base64,', '')
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        image_name = str(timestamp) + '.jpg'
        image_path = 'static/vehicletrace/' + image_name

        try:
            with open(image_path, 'wb') as f:
                f.write(base64.b64decode(image_data))

            processed_image, plate_texts, cropped = process_image(image_path)
            processed_image_path = 'static/vehicletrace/' + 'processed_' + image_name
            cv2.imwrite(processed_image_path, processed_image)

            return JsonResponse({'success': True, 'image_name': image_name, 'plate_texts': plate_texts, 'cropped':cropped})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def index(request):
    return render(request, 'home.html')
  
def logout_us(request):
    logout(request)
    return redirect('/')
    

def home2(request):
    return render(request, 'index.html')

def visitordetail(request):
    return render(request, 'visitordetail.html')

def tracevehicle(request):
    return render(request, 'tracevehicle.html')

def parkschedule(request):
    return render(request, 'parkschedule.html')



def visitor(request):
    if request.method == "GET":
        return render(request, 'visitor.html')
    if request.method == "POST":
        name = request.POST.get('name')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        host = request.POST.get('host')
        purpose = request.POST.get('purpose') 
        current_time = datetime.now()
        vehicle_num = request.POST.get('vehicle_num')
        
        # Create a new instance of the Visitor model
        new_visitor = Visitor.objects.create(name=name,city=city,phone=phone,host=host,purpose=purpose,visit_time=current_time, vehiclenum=vehicle_num)
        new_visitor.save
        return redirect('index/') 
    return render(request, 'visitor.html')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Received username: {username}, password: {password}")  # Debugging

        raw_query = "SELECT * FROM userdata WHERE userid = %s"
        with connection.cursor() as cursor:
            cursor.execute(raw_query, [username])
            row = cursor.fetchone()
            print(f"Database row: {row}")  # Debugging
        
        if row is not None:
            user_id, stored_password = row[0], row[1]
            if password == stored_password:
                request.session['userid'] = username  
                return JsonResponse({'status': 'success', 'output': '1'})
            else:
                return JsonResponse({'status': 'error', 'output': '0'})
        else:
            return JsonResponse({'status': 'error', 'output': '0'})
    
    return JsonResponse({'status': 'error', 'output': '0'})

def getallvisitors(request):
    if request.method == 'POST':
        raw_query = "SELECT * FROM P_visitor"
        with connection.cursor() as cursor:
            cursor.execute(raw_query)
            rows = cursor.fetchall()
        records = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        return JsonResponse(records, safe=False)

def activevehicle(request):
    if request.method == 'POST':
        raw_query = "SELECT * FROM park_vehicle WHERE exit = 0"
        with connection.cursor() as cursor:
            cursor.execute(raw_query)
            rows = cursor.fetchall()
        records = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        return JsonResponse(records, safe=False)

def exitvehicle(request):
    if request.method == 'POST':
        exitnum = request.POST.get('exitnum')

        raw_query = "UPDATE park_vehicle SET exit = 1 WHERE vehiclenumber = %s"
        with connection.cursor() as cursor:
            cursor.execute(raw_query, [exitnum])
        return JsonResponse({'status': 'success', 'message': 'Vehicle exit updated successfully.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def addvisitor(request):
    name = request.POST.get('name')
    address = request.POST.get('address')
    phone = request.POST.get('phone')
    purpose = request.POST.get('purpose')

    current_datetime = datetime.now()
    visit_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    if not (name and address and phone and purpose):
        return JsonResponse({'status': 'error', 'message': 'Missing required data'})
    raw_query = """
    INSERT INTO P_visitor (name, address, phone, visit_time, purpose)
    VALUES (%s, %s, %s, %s, %s)
    """
    with connection.cursor() as cursor:
        cursor.execute(raw_query, [name, address, phone, visit_time, purpose])
        connection.commit()
    return JsonResponse({'status': 'success', 'message': 'Visitor data saved successfully'})

def getseatnum():
    raw_query = """
    SELECT DISTINCT seatnum FROM park_vehicle where exit = 0
    """
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        present_seat_numbers = [int(row[0]) for row in cursor.fetchall()]
    print(present_seat_numbers)
    present_seat_numbers_set = set(present_seat_numbers)
    missing_seat_numbers = [num for num in range(1, 16) if num not in present_seat_numbers_set]
    if len(missing_seat_numbers) > 0:
        return missing_seat_numbers[0]
    else:
        return None

def getallseatnum(request):
    raw_query = """
    SELECT DISTINCT seatnum FROM park_vehicle WHERE exit = 0
    """
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        present_seat_numbers = [int(row[0]) for row in cursor.fetchall()]

    present_seat_numbers_set = list(set(present_seat_numbers))  # Convert set to list

    return JsonResponse({'seats': present_seat_numbers_set})

def addvehicle(request):
    vehiclenumber = request.POST.get('vehiclenumber')
    current_datetime = datetime.now()
    intime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    missingnum = getseatnum()
    
    if missingnum:
        seatnum = missingnum
        exit = 0
        raw_query = """
        INSERT INTO park_vehicle (vehiclenumber, intime, seatnum, exit)
        VALUES (%s, %s, %s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(raw_query, [vehiclenumber, intime, seatnum, exit])
            connection.commit()
        return JsonResponse({'status': 'success', 'message': 'Vehicle parked successfully'})
    else:
        return JsonResponse({'status': 'full', 'message': 'Parking is full.'})


def allotseat(request):
    raw_query = """
    SELECT DISTINCT seatnum FROM park_vehicle where exit = 0
    """
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        present_seat_numbers = [int(row[0]) for row in cursor.fetchall()]
    print(present_seat_numbers)
    present_seat_numbers_set = set(present_seat_numbers)
    missing_seat_numbers = [num for num in range(1, 16) if num not in present_seat_numbers_set]
    if len(missing_seat_numbers) > 0:
        return JsonResponse({'status':'success', 'seat':missing_seat_numbers[0]})
    else:
        return JsonResponse({'status': 'full', 'message': 'Parking is full.'})