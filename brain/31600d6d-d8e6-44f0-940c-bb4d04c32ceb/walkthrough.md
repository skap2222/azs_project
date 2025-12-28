# Gas Station System Walkthrough

## Overview
The Gas Station Management System has been fully implemented with a modern interface featuring both Light and Dark themes, Ukrainian localization, and dynamic fuel type customization.

## Features Implemented

### 1. User Interface (UI/UX)
- **Theme Switcher**: Users can toggle between **Light (Soft)** and **Dark (Neon)** modes via the navbar icon.
- **Dynamic Colors**: Fuel types retain branding colors across themes.
- **Interactive Map**: A new `/map/` page showing station locations with real-time prices.
- **Bonus Shop**: A new `/shop/` page to retrieve rewards.
- **Promotions**: A vibrant `/promotions/` page showcasing current offers.
- **Clean UI**: Simplified pump selection by removing redundant price indicators.
- **Favicon**: Branded gas station icon in the browser tab.

### 2. Backward Logic & Accounts
- **Authentication**: Registration and Login pages.
- **Profiles**: Personal cabinet showing Bonus Balance and Transaction History.
- **Robust Profile Handling**: Profile creation is now fail-safe using `get_or_create`.
- **History**: Detailed table with zebra-striping, custom date format (DD.MM.YYYY HH:MM) using correct `timestamp` field.
- **PDF Receipts**: Users can download a PDF receipt for each transaction.
- **Loyalty System**:
    - **Bonuses**: 1 Liter = 1 Bonus Point.
    - **Coupons**: Transactions >20L trigger a "Free Coffee" reward.
    - **Redemption**: Users can buy Coffee (30) or Hot Dogs (50) in the Shop.

### 3. Backend Logic
- **Models**:
    - `Fuel`: Includes `color_code`.
    - `Pump` & `Transaction`: Business logic.
    - `Profile`: Stores `bonus_balance`, auto-created via signals or view logic.
- **Map**: Uses Leaflet.js with Dark Matter tiles.
- **PDF Generation**: Robust generation using `reportlab` with safe imports.

## Hotfixes Applied
- **Profile Error**: Fixed `RelatedObjectDoesNotExist` by ensuring profile creation in views.
- **Template Error**: Corrected context variables and syntax in `profile.html`.
- **Field Error**: Corrected `created_at` to `timestamp` in queries.

## How to Run
1.  **Ensure Virtual Environment is Active**:
    ```bash
    .\venv\Scripts\activate
    ```
2.  **Run Server**:
    ```bash
    python manage.py runserver
    ```
3.  **Access Site**: Open `http://127.0.0.1:8000`
