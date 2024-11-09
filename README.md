
# Hotel Food Management application

An innovative hotel food management system designed to
 minimize food waste and promote resource sharing among hotels and restaurants. Built using the latest technologies, this app
 allows hotels to notify other establishments about surplus food, facilitating efficient distribution and reducing waste.
## Tech Stack

**Client:** Flutter , Dart

**Server:** Pyhton, FastAPI , WebSocket , MongoDB, MicroService, JWT, Twilio , Cloud

## Prerequisites and Installation

Follow these steps to set up and run the **HotelFood Management (FoodConnect)** project locally.

### Prerequisites

Before you begin, make sure you have the following installed:

1. **Flutter**:
    - Install Flutter by following the [official installation guide](https://flutter.dev/docs/get-started/install).
    - Run the following command to check if Flutter is installed:
      ```bash
      flutter doctor
      ```

2. **Firebase Account and Project Setup**:
    - Create a Firebase project in the [Firebase Console](https://console.firebase.google.com/).
    - Enable the following Firebase services:
      - Firestore (for data storage)
      - Firebase Authentication (for user login)
      - Firebase Cloud Messaging (for push notifications)
    - Download the `google-services.json` file for Android or `GoogleService-Info.plist` for iOS.

3. **Twilio Account** (for SMS and call functionalities):
    - Create an account on [Twilio](https://www.twilio.com/).
    - Get your **Account SID** and **Auth Token** from your Twilio Console.

4. **MongoDB** (for backend data storage, if using):
    - Make sure MongoDB is installed and running on your local machine, or use a hosted MongoDB service like [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).

### Clone the Repository

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/your-username/foodconnect.git
cd foodconnect

## Demo

Insert gif or link to demo


## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

## Running Tests

To run tests, run the following command:

```bash
flutter test
