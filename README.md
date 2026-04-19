# edge_password_recovery
# Microsoft Edge Password Recovery Tool

A Python tool to extract saved passwords, autofill data, and payment information from Microsoft Edge (Chromium-based) browser on Windows.

## 📋 Overview

This tool decrypts and extracts stored credentials from Microsoft Edge's local database files, including:
- Saved login credentials (usernames/passwords)
- Autofill form data
- Credit card/payment information

## ⚠️ Legal Disclaimer

**This tool is for educational and authorized security testing purposes only.**
- Only use this tool on systems you own or have explicit permission to test
- Extracting passwords from browsers without consent may violate privacy laws and terms of service
- The author assumes no liability for misuse of this tool

## 🔧 Requirements

### System Requirements
- Windows operating system (uses Windows DPAPI)
- Microsoft Edge (Chromium-based) installed
- Python 3.7 or higher

### Python Dependencies
```
pywin32
pycryptodome
```

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/crackkillz/edge_password_recovery.git
cd edge_password_recovery
```

### 2. Install Required Packages

Using pip:
```bash
pip install pywin32 pycryptodome
```

Or using requirements.txt:
```bash
pip install -r requirements.txt
```

Create `requirements.txt`:
```
pywin32==306
pycryptodome==3.20.0
```

## 🚀 Usage

### Basic Usage
```bash
python edge_password_recovery.py
```

### Important Notes
1. **Close Microsoft Edge completely** before running the script
   - Check Task Manager to ensure no Edge processes are running
   - The database files are locked when Edge is open

2. **Run with appropriate permissions**
   - The script needs read access to Edge's user data directory
   - Standard user permissions are sufficient for your own profile

### Sample Output
```
Microsoft Edge Password Recovery Tool
==================================================
Note: This tool requires Edge to be closed to access the databases.
==================================================

Press Enter to continue...

==================================================
EDGE BROWSER DATA
==================================================

📝 LOGINS:
  URL: https://github.com
  Username: crackkillz
  Password: example_password123

  URL: https://mail.google.com
  Username: user@gmail.com
  Password: another_password

🔧 AUTOFILL:
  Name: address
  Value: 123 Main Street

💳 PAYMENT DATA:
  Name on Card: John Doe
  Expiration Month: 12
  Expiration Year: 2025
  Card Number: 4111111111111111
```

## 🗂️ File Structure

```
edge-password-recovery/
├── edge_password_recovery.py   # Main script
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── LICENSE                      # License information
```

## 🔍 How It Works

1. **Locates Edge Data**: Finds Edge's user data directory at `%LocalAppData%\Microsoft\Edge\User Data\`

2. **Extracts Master Key**: Retrieves the encrypted master key from `Local State` file and decrypts it using Windows DPAPI

3. **Decrypts Database**: Opens SQLite database files (`Login Data`, `Web Data`) containing saved credentials

4. **Decrypts Passwords**: Uses AES-256-GCM decryption with the master key to decrypt password values

5. **Displays Results**: Outputs all recovered data in readable format

## 🛠️ Troubleshooting

### Error: "File not found"
- Ensure Microsoft Edge is installed
- Check if you're using Edge Beta/Dev/Canary (script auto-detects these)
- Verify the correct user profile path

### Error: "Database is locked"
- Close all Edge windows and processes
- Check Task Manager for background Edge processes
- Restart computer if necessary

### Error: "Failed to decrypt"
- Ensure Edge was closed before extracting data
- The master key might have changed (Edge updates can affect this)
- Try running as the same user who created the data

### Error: "No module named 'win32crypt'"
```bash
pip install pywin32
```

### Error: "No module named 'Crypto'"
```bash
pip install pycryptodome
```

## 🔐 Security Considerations

- The script requires the same user context as Edge's data to decrypt passwords
- Master keys are protected by Windows DPAPI tied to your user account
- Decrypted passwords are displayed in plain text in the console
- Consider using this in secure, offline environments

## 📝 Edge Versions Supported

- Microsoft Edge Stable
- Microsoft Edge Beta
- Microsoft Edge Dev
- Microsoft Edge Canary

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**crackkillz**
- GitHub: [@crackkillz](https://github.com/crackkillz)

## ⭐ Support

If you find this tool useful, please give it a star on GitHub!

## ❓ FAQ

**Q: Does this work on other browsers?**
A: The code can be adapted for Chrome, Brave, Opera, and other Chromium-based browsers by changing the path.

**Q: Can I export the data to a file?**
A: Yes, modify the script to write output to a text file instead of console.

**Q: Does this work on Linux/Mac?**
A: No, this version uses Windows DPAPI. Linux/Mac versions would need different decryption methods.

**Q: Why do I need to close Edge?**
A: Edge locks the SQLite database files when running, preventing read access.

**Q: Is my data sent anywhere?**
A: No, this script runs entirely locally and doesn't transmit any data.

---

**⚠️ REMINDER: Only use this tool on systems you own or have explicit permission to test. Unauthorized access to others' credentials is illegal and unethical.**
