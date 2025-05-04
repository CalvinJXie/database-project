# database-project

Database project to implement a stock visualization with login.

### Brief Description of How to Install and Use the System

Follow these steps to install, launch, and use the system:

1. **Install MySQL Local Server**  
   Download and install MySQL Community Server from the official website. Choose the version suitable for your OS and follow the setup instructions.

2. **Launch the MySQL Server**  
   Open a terminal and run:
   ```bash
   mysql -u root -p --local-infile --enable-system-command
   ```
   When prompted, enter:
   ```
   Password: Hello123#
   ```

3. **Start the Frontend Web Interface**  
   Change into the project directory and start the frontend server:
   ```bash
   cd money_maker
   npm run dev
   ```
   Open your browser and go to:
   ```
   http://localhost:3000/sign-in
   ```

4. **Launch the Backend Server**  
   Navigate back to your home directory and start the backend server:
   ```bash
   cd ~
   python server/app.py
   ```

5. **Create Database Tables**  
   Run the following SQL script to create all required tables:
   ```sql
   source ~/git/database-project/SQL/create.sql;
   ```

6. **Load Sample Data**  
   Populate the database with initial sample data:
   ```sql
   source ~/git/database-project/SQL/load.sql;
   ```

Once these steps are complete, your database system will be fully installed and running with both backend and frontend servers connected to a MySQL database.
