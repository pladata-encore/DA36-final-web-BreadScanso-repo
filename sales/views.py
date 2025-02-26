from django.shortcuts import render

def sales_main(request):
    # 더미 데이터
    sales_data = {
        "daily": [
            {"date": "2025-02-10", "sales": 50000},
            {"date": "2025-02-11", "sales": 62000},
            {"date": "2025-02-12", "sales": 54000},
            {"date": "2025-02-13", "sales": 58000},
            {"date": "2025-02-14", "sales": 60000},
            {"date": "2025-02-15", "sales": 63000},
            {"date": "2025-02-16", "sales": 70000}
        ],
        "top5": [
            {"id": "1", "name": "단팥빵", "quantity": 10, "total_price": 50000},
            {"id": "2", "name": "소금빵", "quantity": 8, "total_price": 40000},
            {"id": "3", "name": "식빵", "quantity": 7, "total_price": 35000},
            {"id": "4", "name": "커스터드크림빵", "quantity": 6, "total_price": 30000},
            {"id": "5", "name": "피자빵", "quantity": 5, "total_price": 25000}
        ]
    }
    # GET 요청 처리 (member 데이터 가져오기)
    member = request.user.member

    # 하나의 딕셔너리로 합쳐서 전달
    context = {
        'sales_data': sales_data,
        'member': member
    }

    return render(request, 'sales/sales_main.html', context)

