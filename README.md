# Smart Inventory Management System

A simple Python and SQLite inventory management CLI application for tracking products, sales, stock purchases, and low-stock alerts.

## Features

- Admin login with default credentials:siddiq\siddiq
- Add new products with category, price, quantity, and supplier
- Sell products with stock validation and automatic quantity updates
- Purchase stock to increase inventory
- Search products by name or category
- View today's sales total
- Display top selling products
- Dashboard showing:
  - total products
  - available stock
  - low stock items
  - today's sales
  - top 5 selling products

## Getting Started

1. Install Python 3.10+.
2. Open a terminal in the project folder.
3. Run:

```bash
python inventory.py
```

4. Login using:

- Username: `siddiq`
- Password: `siddiq`

## Notes

- The application uses `inventory.db` in the same folder.
- The first run creates the database and default admin user.
- Use the menu to manage products and sales.
images(flow of working project, ongoing with every feature)

1.ADD Product
<img width="955" height="591" alt="Screenshot 2026-07-20 102847" src="https://github.com/user-attachments/assets/cac2ab68-d691-464f-ad0b-555d53155007" />

2.Sell Product
<img width="882" height="590" alt="Screenshot 2026-07-20 103010" src="https://github.com/user-attachments/assets/1bd8507f-8907-4b7b-b21d-9ddd8eed60d9" />

3.Purchase Stock
<img width="792" height="505" alt="Screenshot 2026-07-20 103106" src="https://github.com/user-attachments/assets/f1a5351b-6a86-44a8-ad61-7c9f8d684edd" />

4.)Search Product
<img width="828" height="621" alt="Screenshot 2026-07-20 103157" src="https://github.com/user-attachments/assets/9a42dc69-e08a-4a63-a171-20e6f069edee" />

5.)Today's Sales

<img width="647" height="282" alt="Screenshot 2026-07-20 103221" src="https://github.com/user-attachments/assets/8698ee1c-1294-4fa7-9258-c3487a7009fb" />

6.)Top Selling Products

<img width="668" height="322" alt="Screenshot 2026-07-20 103246" src="https://github.com/user-attachments/assets/be69d409-df04-4377-a7f6-1beeb558fe0a" />

7.)Dash Board

<img width="712" height="490" alt="Screenshot 2026-07-20 103323" src="https://github.com/user-attachments/assets/dc1e6a78-259d-4677-9328-9ab6635b3093" />


## Extending the Project

Possible additions for a portfolio-ready version:

- A web dashboard built with Flask or FastAPI
- Export reports to CSV
- Role-based access with employee vs admin privileges
- Supplier management and purchase orders
- Graphical charts for sales trends
