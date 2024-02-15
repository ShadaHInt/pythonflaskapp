from flask import Blueprint , render_template,request,flash,redirect, url_for
import pyodbc
auth = Blueprint('auth', __name__)

def connection():
    cstr = f'DRIVER={{SQL Server}};SERVER=SHADAN\SQLEXPRESS;DATABASE=UserNew;'
    conn = pyodbc.connect(cstr)
    return conn

@auth.route('/')
def home():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.UsersList")
    user_data = cursor.fetchall()
    conn.close()
    return render_template("home.html",user_data=user_data)

@auth.route('/Adduser', methods=['GET', 'POST'])
def Adduser():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        country = request.form.get('country')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        address = request.form.get('address')
        state = request.form.get('state')

        # Data for UserList table
        user_list_data = (first_name, last_name, gender, email, phone, address, country, state)

        qualification_list = request.form.getlist('qualification[]')
        year_list = request.form.getlist('year[]')
        university_list = request.form.getlist('university[]')
        grade_list = request.form.getlist('grade[]')

        num_qualifications = min(len(qualification_list), len(year_list), len(university_list), len(grade_list))

        qualifications = []
        for i in range(num_qualifications):
            qualification = qualification_list[i]
            year = year_list[i]
            university = university_list[i]
            grade = grade_list[i]

            # Check if all fields for this qualification are non-empty
            if qualification and year and university and grade:
                qualifications.append((qualification, year, university, grade))

        conn = connection()
        cursor = conn.cursor()

        try:
            # Insert data into UsersList table
            user_query = """
                INSERT INTO UsersList (FirstName, LastName, Gender, Email, Phone, ContactAddress, Country, States)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(user_query, user_list_data)

            # Get the UserID of the newly inserted user
            cursor.execute("SELECT @@IDENTITY")
            user_id = cursor.fetchone()[0]

            # Insert data into UserQualification table
            qualification_query = """
                INSERT INTO UserQualification (UserID, Qualification, YearOfPassing, University, GradePercentage)
                 VALUES (?, ?, ?, ?, ?)
            """
            for qualification_data in qualifications:
                # Construct the parameter tuple for the qualification_query
                params = (user_id,) + qualification_data
                cursor.execute(qualification_query, params)

            conn.commit()
            conn.close()

            flash('Account created!', category='success')
            return redirect(url_for('auth.home'))  # Redirect to the same page after successful insertion
        except Exception as e:
            # Handle exceptions (e.g., database errors) and set an error flash message
            flash('An error occurred while adding the user. Please try again later.', category='error')
            return redirect(url_for('auth.Adduser'))

    return render_template("adduser.html")

@auth.route('/Viewuser<int:UserID>', methods=['GET', 'POST'])
def view(UserID):
    # Fetch user details based on user_id from the database
    conn = connection()
    cursor = conn.cursor()
    user_query = "SELECT * FROM UsersList WHERE UserID = ?"
    cursor.execute(user_query, UserID)
    user = cursor.fetchone()  # Assuming one user per user_id

    qualification_query = "SELECT * FROM UserQualification WHERE UserID = ?"
    cursor.execute(qualification_query, (UserID,))
    qualifications = cursor.fetchall()

    conn.close()

    return render_template("viewuser.html", user=user, qualifications=qualifications)

@auth.route('/Edituser/<int:UserID>', methods=['GET', 'POST'])
def edituser(UserID):
    # Fetch user details based on user_id from the database
    conn = connection()
    cursor = conn.cursor()
    user_query = "SELECT * FROM UsersList WHERE UserID = ?"
    cursor.execute(user_query, UserID)
    user = cursor.fetchone()

    qualification_query = "SELECT * FROM UserQualification WHERE UserID = ?"
    cursor.execute(qualification_query, UserID)
    qualifications = cursor.fetchall()

    if request.method == 'POST':
        # Handle form submission with updated user information

        # Retrieve updated user information from the form
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        gender = request.form.get('gender')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        country = request.form.get('country')
        state = request.form.get('state')

        # Update the user's information in the database
        update_query = """
            UPDATE UsersList
            SET FirstName = ?, LastName = ?, Gender = ?, Email = ?, Phone = ?, ContactAddress = ?, Country = ?, States = ?
            WHERE UserID = ?
        """
        cursor.execute(update_query, (first_name, last_name, gender, email, phone, address, country, state, UserID))
        conn.commit()

        # Update qualification details
        for qualification in qualifications:
            user_id = qualification.UserID  # Retrieve the user's ID associated with the qualification
            qual_key = f'qualification_{user_id}'  # Use user_id instead of qid
            year_key = f'year_{user_id}'  # Use user_id instead of qid
            university_key = f'university_{user_id}'  # Use user_id instead of qid
            grade_key = f'grade_{user_id}'  # Use user_id instead of qid

            qualification_val = request.form.get(qual_key)
            year_val = request.form.get(year_key)
            university_val = request.form.get(university_key)
            grade_val = request.form.get(grade_key)

            update_qual_query = """
                UPDATE UserQualification
                SET Qualification = ?, YearOfPassing = ?, University = ?, GradePercentage = ?
                WHERE  UserID = ?
            """
            print("Executing the following SQL query:")
            print(update_qual_query)
            print("Parameters:")
            print(f"Qualification: {qualification_val}")
            print(f"YearOfPassing: {year_val}")
            print(f"University: {university_val}")
            print(f"GradePercentage: {grade_val}")
            print(f"UserID: {UserID}")

            cursor.execute(update_qual_query, (qualification_val, year_val, university_val, grade_val,  UserID))
            conn.commit()

        return redirect(url_for('auth.view', UserID=UserID))  # Redirect to view the updated user

    return render_template("edituser.html", user=user, qualifications=qualifications)

@auth.route('/DeleteUser/<int:UserID>', methods=['GET', 'POST'])
def delete(UserID):
    # Connect to the database
    conn = connection()
    cursor = conn.cursor()

    # Delete the user's qualifications first
    delete_qualifications_query = "DELETE FROM UserQualification WHERE UserID = ?"
    cursor.execute(delete_qualifications_query, (UserID,))
    conn.commit()

    # Then delete the user from the UsersList table
    delete_user_query = "DELETE FROM UsersList WHERE UserID = ?"
    cursor.execute(delete_user_query, (UserID,))
    conn.commit()

    conn.close()

    # Redirect to a page after deletion, e.g., the home page
    return redirect(url_for('auth.home'))

