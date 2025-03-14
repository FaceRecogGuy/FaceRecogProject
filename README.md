# **Setting Up AWS & Boto3**

**Warning:** As this uses boto3 from AWS, you will have to sign up for Amazon Web Services with your credit card.

## **Assumptions**
- Any command prompt command was performed by opening your computer’s command prompt as an administrator.
- All steps were performed without the use of a virtual environment.

---

## **Setup**
1. Start by downloading `boto3.py` and `verify.py`.
2. Create a new folder for the whole project and name it appropriately.
3. Move `testBoto3.py` into this new folder.
4. Inside your newly created folder, create the following subfolders:
   - `known_faces`
   - `new_faces`

---

## **1️⃣ Create an AWS Account**  
1. Go to **[AWS Signup](https://aws.amazon.com/)**  
2. Click **"Create an AWS Account"**  
3. Enter your email, choose an AWS account name, and set a password  
4. Select **Personal or Business account**  
5. Enter your billing details (AWS requires a payment method, but Free Tier is available)  
6. Complete identity verification via phone OTP  
7. Choose a **Support Plan** (select **Free Tier**)  
8. Click **"Complete Signup"**  

---

## **2️⃣ Create an IAM User for Secure Access**  
1. **Log in** to AWS and go to the **IAM Console**:  
   - [IAM Users](https://console.aws.amazon.com/iam/home#/users)  
2. Click **"Add User"**  
3. Enter a **Username** (e.g., `boto3-user`)  
4. Select **Programmatic access**  
5. Click **Next: Permissions**  

### **Assign IAM Permissions**  
- **Method 1 (Recommended): Attach Policies Directly**  
  - `AmazonRekognitionFullAccess` (for Rekognition)  
  - `IAMReadOnlyAccess` (for viewing user info)  

6. Click **Next: Review** → **Create User**  
7. **Download the Access Key & Secret Key** (Save it securely!)  

---

## **3️⃣ Install & Configure AWS CLI**  
**Install AWS CLI** (if not installed)  
- **Windows**: Download the .msi file from [AWS CLI Installer](https://aws.amazon.com/cli/)  
- **Mac/Linux**:  
  ```sh
  curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
  sudo installer -pkg AWSCLIV2.pkg -target /
  ```

**Verify Installation:**  
```sh
aws --version
```

**Configure AWS CLI with IAM Credentials:**  
```sh
aws configure
```
Enter:  
- **AWS Access Key ID** (from IAM user)  
- **AWS Secret Access Key**  
- **Default region** (e.g., `ap-southeast-1`)  
- **Output format**: `json` (or leave blank)  

**Verify Setup**  
```sh
aws sts get-caller-identity
```
Expected output:  
```json
{
    "UserId": "AIDAEXAMPLE123456789",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/boto3-user"
}
```

---

## **4️⃣ Install & Configure Boto3 in Python**  
### **Install Boto3 & Dependencies**  
```sh
pip install boto3
```

### **Verify Boto3 Installation**  
Run  
```sh
python verify.py
```
If working, it should print **UserId, Account, and ARN** and `{ "CollectionIds": [] }`.

---

## **5️⃣ The Actual Project Setup**  
Run the following commands:  
```sh
pip install boto3
pip install opencv-python
pip install numpy
```
**Note:** This documentation was performed on a windows PC with proper Python installation, and all three commands were executed without issues.

You do not need to put any faces into the `known_faces` folder, but if you do, try using your own. If these images do not show up in the ‘Known faces:’ print statement, retry in an environment with good lighting.

Expect your face to be framed by a red square labelled `unknown` if you did not put any images in `known_faces`. If you did and it recognises your face, it will label the square as whatever you've named the image.

---

Your setup is now complete!

# code from https://youtu.be/tl2eEBFEHqM?si=WDNKmpL3BWeqJPOZ
