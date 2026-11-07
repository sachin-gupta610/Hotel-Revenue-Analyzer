import os
import pandas as pd
import matplotlib.pyplot as plt

def load_and_clean_data(filename):
    if not os.path.exists(filename):
        print(f"(b) Error: File '{filename}' not found.")
        return None

    try:
        df = pd.read_csv(filename)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    valid_rows = []
    
    for idx, row in df.iterrows():
        row_num = idx + 2  # CSV header ke baad 1-based row index
        
        # Check non-numeric ya negative values
        try:
            rooms = float(row['RoomsSold'])
            rate = float(row['Rate'])
            
            if rooms < 0 or rate < 0:
                print(f"Warning: Row {row_num} skipped - RoomsSold must be 0 or more.")
                continue
            
            valid_rows.append({
                'Date': str(row['Date']).strip(),
                'RoomType': str(row['RoomType']).strip(),
                'RoomsSold': rooms,
                'Rate': rate,
                'Revenue': rooms * rate
            })
        except (ValueError, TypeError):
            print(f"Warning: Row {row_num} skipped - Invalid non-numeric values found.")
            continue

    clean_df = pd.DataFrame(valid_rows)
    return clean_df

def show_daily_revenue(df):
    daily = df.groupby('Date')['Revenue'].sum()
    total_rev = daily.sum()
    best_day = daily.idxmax()
    best_day_rev = daily.max()

    for date, rev in daily.items():
        print(f"{date} : Rs. {int(rev)}")
    print(f"Total revenue: Rs. {int(total_rev)}")
    print(f"Best day: {best_day} (Rs. {int(best_day_rev)})")

    # Chart display
    daily.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Daily Revenue')
    plt.xlabel('Date')
    plt.ylabel('Revenue (Rs.)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_revenue_by_room_type(df):
    room_rev = df.groupby('RoomType')['Revenue'].sum()
    total_rev = room_rev.sum()

    for r_type, rev in room_rev.items():
        pct = (rev / total_rev) * 100
        print(f"{r_type} : Rs. {int(rev)} ({pct:.2f}%)")
    print(f"Total revenue: Rs. {int(total_rev)}")

    # Pie Chart
    room_rev.plot(kind='pie', autopct='%1.2f%%', startangle=90)
    plt.title('Revenue Share by Room Type')
    plt.ylabel('')
    plt.tight_layout()
    plt.show()

def main():
    filename = input("Enter CSV filename (default: hotel_sales.csv): ").strip()
    if not filename:
        filename = "hotel_sales.csv"

    df = load_and_clean_data(filename)
    if df is None or df.empty:
        return

    print(f"Valid records analysed: {len(df)}")
    print("\nSelect Option:")
    print("1. Daily revenue")
    print("2. Revenue by room type")
    
    choice = input("Enter choice (1/2): ").strip()
    print("-" * 30)

    if choice == "1":
        show_daily_revenue(df)
    elif choice == "2":
        show_revenue_by_room_type(df)
    else:
        print("Invalid Choice.")

if __name__ == "__main__":
    main()