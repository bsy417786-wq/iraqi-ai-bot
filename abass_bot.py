import openpyxl
from datetime import datetime

def add_order_to_excel(name, phone, order_item, selling_price):
    # 1. نحدد تكلفة المنتجات (تقدر تخليها بملف ثاني بعدين)
    # مثال: التيشيرت تكلفته 10، والبنطلون 15
    product_costs = {
        "تيشيرت": 10000,
        "بنطلون": 15000,
        "قميص": 12000
    }

    # 2. عباس يشوف التكلفة حسب نوع الطلب
    # إذا المنتج مو موجود بالقائمة، يخلي التكلفة صفر حتى صاحب المحل يمليها
    cost_price = product_costs.get(order_item, 0)

    # 3. فتح ملف الإكسل اللي رتبته (A إلى H)
    wb = openpyxl.load_workbook('orders.xlsx')
    sheet = wb.active

    # 4. البحث عن أول سطر فارغ
    next_row = sheet.max_row + 1

    # 5. توزيع البيانات على الأعمدة اللي رتبتها (A إلى H)
    sheet[f'A{next_row}'] = datetime.now().strftime("%Y-%m-%d %H:%M") # الوقت
    sheet[f'B{next_row}'] = name           # الاسم
    sheet[f'C{next_row}'] = phone          # الرقم
    sheet[f'D{next_row}'] = order_item     # الطلب
    sheet[f'E{next_row}'] = "قيد الانتظار" # حالة الطلب
    sheet[f'F{next_row}'] = selling_price  # سعر البيع
    sheet[f'G{next_row}'] = cost_price     # سعر التكلفة (عباس جابها وحده!)
    
    # ملاحظة: حرف H فيه معادلة بالإكسل راح تحسب الربح تلقائياً

    # 6. حفظ الملف
    wb.save('orders.xlsx')
    print(f"تم بنجاح! عباس نزل طلب {name} وحسب التكلفة {cost_price}")

# --- تجربة الكود ---
# تخيل عباس استلم رسالة: "أريد تيشيرت، اسمي عباس حيدر ورقمي 0770..."
add_order_to_excel("عباس حيدر", "07700000000", "تيشيرت", 25000)
