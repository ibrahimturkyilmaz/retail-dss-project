
def calculate_loyalty_points(total_amount: float, shopping_count: int) -> float:
    """
    Alışveriş sayısına göre puan hesaplar.
    Mantik: 
    1. Alışveriş -> 1x Puan (1 TL = 1 Puan)
    2. Alışveriş -> 2x Puan
    3. Alışveriş -> 3x Puan
    ...
    Max 5x ile sınırlandırılabilir.
    """
    
    multiplier = shopping_count
    
    # Yeni alışveriş olduğu için count henüz artmamış olabilir, 
    # bu yüzden o anki işlem sırasına göre katsayı veriyoruz.
    # Eğer shopping_count geçmiş alışveriş sayısı ise, bu işlem (old_count + 1) olur.
    # Biz buraya "bu kaçıncı alışveriş?" değerini bekliyoruz.
    
    if multiplier < 1:
        multiplier = 1
        
    if multiplier > 5:
        multiplier = 5 # Tavan sınır
        
    points = total_amount * multiplier
    return points
