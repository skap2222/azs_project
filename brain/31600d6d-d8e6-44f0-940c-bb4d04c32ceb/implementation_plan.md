# Gas Station Management System - Implementation Plan

## Goal Description
Implement PDF receipt generation for transactions and allow users to download them from their profile.

## User Review Required
- **Receipt Design**: Will use ReportLab to generate a clean PDF with logo and transaction details.
- **Button**: Violet/Turquoise button in profile history.

## Proposed Changes

### Dependencies
- Install `reportlab`.

### Backend
- **`views.py`**: Add `download_receipt(request, transaction_id)`.
    - Verify `transaction.user == request.user`.
    - Generate PDF using `reportlab`.
    - Return `FileResponse`.
- **`urls.py`**: Add path `receipt/<int:transaction_id>/`.

### Frontend
- **`profile.html`**: Add "Action" column to history table with "Download PDF" button.

## Verification Plan
### Manual Verification
1. **Profile**: Check for "Download Receipt" button.
2. **Download**: Click button, verify PDF downloads.
3. **Content**: Open PDF, check for Logo, Date, Pump, Fuel, Price, Liters, Amount, Bonuses, Footer.
