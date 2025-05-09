from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # needed for sessions

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Friday@786',
    'database': 'Bank_Managment_System_Project'
}

# Function to get a database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            conn.autocommit = True
            return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.callproc('LoginSystem', [username, password])
                for result in cursor.stored_results():
                    status = result.fetchall()[0][0]

                if status == 'Login Successfull':
                    # Check the user's role
                    cursor.execute("SELECT role FROM users WHERE username = %s", (username,))
                    role = cursor.fetchone()[0]
                    session['username'] = username
                    session['role'] = role
                    flash('Login Successful!', 'success')
                    if role == 'Admin':
                        return redirect(url_for('admin_dashboard'))
                    return redirect(url_for('menu'))
                else:
                    flash('Login Failed! Check your username or password.', 'danger')
            except Error as e:
                flash(f"Error: {e}", 'danger')
            finally:
                cursor.close()
                conn.close()
    return render_template('login.html')

@app.route('/menu')
def menu():
    if 'username' not in session:
        flash('Please log in to access the menu.', 'danger')
        return redirect(url_for('login'))
    return render_template('menu.html', role=session.get('role'))

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if 'username' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.callproc('InsertCustomer', [name, email, phone])
                for result in cursor.stored_results():
                    flash(result.fetchall()[0][0], 'info')
            except Error as e:
                flash(f"Error: {e}", 'danger')
            finally:
                cursor.close()
                conn.close()
    return render_template('add_customer.html')

@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    if 'username' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        cust_id = request.form['customer_id']
        balance = request.form['balance']
        account_type = request.form['account_type']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.callproc('InsertAccount', [cust_id, balance, account_type])
                for result in cursor.stored_results():
                    flash(result.fetchall()[0][0], 'info')
            except Error as e:
                flash(f"Error: {e}", 'danger')
            finally:
                cursor.close()
                conn.close()
    return render_template('add_account.html')

@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if 'username' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        acc_id = request.form['account_id']
        amount = request.form['amount']
        trans_type = request.form['transaction_type']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.callproc('InsertTransactions', [acc_id, amount, trans_type])
                for result in cursor.stored_results():
                    flash(result.fetchall()[0][0], 'info')
            except Error as e:
                flash(f"Error: {e}", 'danger')
            finally:
                cursor.close()
                conn.close()
    return render_template('transaction.html')

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'username' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        from_acc = request.form['from_account']
        to_acc = request.form['to_account']
        amount = request.form['amount']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.callproc('TransferAccount', [from_acc, to_acc, amount])
                for result in cursor.stored_results():
                    flash(result.fetchall()[0][0], 'info')
            except Error as e:
                flash(f"Error: {e}", 'danger')
            finally:
                cursor.close()
                conn.close()
    return render_template('transfer.html')

@app.route('/add_loan', methods=['GET', 'POST'])
def add_loan():
    if 'username' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        cust_id = request.form['customer_id']
        loan_amount = request.form['loan_amount']
        interest_rate = request.form['interest_rate']
        loan_term = request.form['loan_term']
        loan_status = request.form['loan_status']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.callproc('InsertLoan', [cust_id, loan_amount, interest_rate, loan_term, loan_status])
                for result in cursor.stored_results():
                    flash(result.fetchall()[0][0], 'info')
            except Error as e:
                flash(f"Error: {e}", 'danger')
            finally:
                cursor.close()
                conn.close()
    return render_template('add_loan.html')

@app.route('/update_loan', methods=['GET', 'POST'])
def update_loan():
    if 'username' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        loan_id = request.form['loan_id']
        new_status = request.form['new_status']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.callproc('UpdateLoanStatus', [loan_id, new_status])
                for result in cursor.stored_results():
                    flash(result.fetchall()[0][0], 'info')
            except Error as e:
                flash(f"Error: {e}", 'danger')
            finally:
                cursor.close()
                conn.close()
    return render_template('update_loan.html')

@app.route('/view_accounts')
def view_accounts():
    if 'username' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM AccountSummary')
            accounts = cursor.fetchall()
            return render_template('view_accounts.html', accounts=accounts)
        except Error as e:
            flash(f"Error: {e}", 'danger')
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('menu'))

@app.route('/view_customers')
def view_customers():
    if 'username' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM View_Total_Accounts_Customer')
            customers = cursor.fetchall()
            return render_template('view_customers.html', customers=customers)
        except Error as e:
            flash(f"Error: {e}", 'danger')
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('menu'))

@app.route('/view_loans')
def view_loans():
    if 'username' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)  # Using dictionary cursor to access column names easily
        try:
            cursor.execute('SELECT * FROM loans')
            loans = cursor.fetchall()

            # Calculate loan interest for each loan
            for loan in loans:
                loan['loan_interest'] = loan['loan_amount'] * loan['interest_rate'] / 100  # Interest calculation

            return render_template('view_loans.html', loans=loans)
        except Error as e:
            flash(f"Error: {e}", 'danger')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('menu'))



@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' not in session or session.get('role') != 'Admin':
        flash('Please log in as an admin to access the dashboard.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed.', 'danger')
        return redirect(url_for('login'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Fetch Admin Overview
        cursor.execute("SELECT * FROM AdminOverview")
        overview = cursor.fetchone()
        
        # Fetch All Transactions
        cursor.callproc('ViewAllTransactions')
        for result in cursor.stored_results():
            transactions = result.fetchall()
        
        # Fetch all accounts for freeze/unfreeze
        cursor.execute("SELECT a.account_id, a.customer_id, c.name AS customer_name, a.balance, a.account_type, a.status "
                      "FROM accounts a JOIN customers c ON a.customer_id = c.customer_id")
        accounts = cursor.fetchall()
        
        return render_template('admin_dashboard.html', overview=overview, transactions=transactions, accounts=accounts)
    
    except Error as e:
        flash(f"Error: {e}", 'danger')
        return redirect(url_for('login'))
    finally:
        cursor.close()
        conn.close()

@app.route('/freeze_account/<int:account_id>/<string:action>')
def freeze_account(account_id, action):
    if 'username' not in session or session.get('role') != 'Admin':
        flash('Please log in as an admin to perform this action.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed.', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    try:
        cursor = conn.cursor()
        new_status = 'Frozen' if action == 'freeze' else 'Active'
        cursor.callproc('FreezeAccount', (account_id, new_status))
        for result in cursor.stored_results():
            status = result.fetchall()[0][0]
        flash(status, 'info')
    except Error as e:
        flash(f"Error: {e}", 'danger')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)