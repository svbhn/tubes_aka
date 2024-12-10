import time
import random
from typing import List
from tqdm import tqdm

class Mahasiswa:
    def __init__(self, nim: int, nama: str, ipk: float):
        self.nim = nim
        self.nama = nama
        self.ipk = ipk

class SortingAlgorithm:
    @staticmethod
    def quicksort(arr: List[Mahasiswa], key: str) -> List[Mahasiswa]:
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        left = []
        middle = []
        right = []
        
        for x in arr:
            value = getattr(x, key)
            pivot_value = getattr(pivot, key)
            
            if value < pivot_value:
                left.append(x)
            elif value == pivot_value:
                middle.append(x)
            else:
                right.append(x)
        
        return SortingAlgorithm.quicksort(left, key) + middle + SortingAlgorithm.quicksort(right, key)
    
    @staticmethod
    def mergesort(arr: List[Mahasiswa], key: str) -> List[Mahasiswa]:
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = SortingAlgorithm.mergesort(arr[:mid], key)
        right = SortingAlgorithm.mergesort(arr[mid:], key)
        
        return SortingAlgorithm.merge(left, right, key)
    
    @staticmethod
    def merge(left: List[Mahasiswa], right: List[Mahasiswa], key: str) -> List[Mahasiswa]:
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if getattr(left[i], key) <= getattr(right[j], key):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result

def generate_data(n: int) -> List[Mahasiswa]:
    """Menghasilkan data mahasiswa acak"""
    nama_depan = ["Andi", "Budi", "Citra", "Deni", "Eka"]
    nama_belakang = ["Pratama", "Wijaya", "Sari", "Putra", "Dewi"]
    
    data = []
    for _ in range(n):
        nim = random.randint(10000000, 99999999)
        nama = f"{random.choice(nama_depan)} {random.choice(nama_belakang)}"
        ipk = round(random.uniform(2.0, 4.0), 2)
        data.append(Mahasiswa(nim, nama, ipk))
    
    return data

def measure_time(algorithm, data: List[Mahasiswa], key: str, runs: int = 3) -> float:
    """Mengukur waktu rata-rata dari beberapa kali pengujian"""
    times = []
    for _ in range(runs):
        data_copy = data.copy()
        start_time = time.time()
        algorithm(data_copy, key)
        times.append(time.time() - start_time)
    return sum(times) / runs

def get_user_input() -> List[int]:
    """Meminta input dari user untuk ukuran data yang akan dianalisis"""
    input_sizes = []
    
    while True:
        try:
            n = int(input("Masukkan jumlah data yang ingin dianalisis (0 untuk selesai): "))
            if n == 0:
                break
            if n < 0:
                print("Jumlah data tidak boleh negatif!")
                continue
            input_sizes.append(n)
        except ValueError:
            print("Input harus berupa angka!")
            continue
    
    if not input_sizes:
        print("Menggunakan ukuran default...")
        return [1, 10, 20, 50, 100, 200, 500, 1000]
    
    return sorted(input_sizes)  # Mengurutkan input untuk visualisasi yang lebih baik

def analyze_complexity(input_sizes: List[int]):
    # Menyimpan hasil waktu eksekusi
    quicksort_times = []
    mergesort_times = []
    
    print("\nMenganalisis kompleksitas algoritma...")
    
    # Mengukur waktu untuk setiap ukuran input
    for size in tqdm(input_sizes):
        data = generate_data(size)
        
        # Mengukur waktu Quicksort
        quick_time = measure_time(SortingAlgorithm.quicksort, data, 'nim')
        quicksort_times.append(quick_time)
        
        # Mengukur waktu Mergesort
        merge_time = measure_time(SortingAlgorithm.mergesort, data, 'nim')
        mergesort_times.append(merge_time)
    
    return {
        'input_sizes': input_sizes,
        'quicksort_times': quicksort_times,
        'mergesort_times': mergesort_times
    }

def main():
    print("Selamat datang di program analisis kompleksitas algoritma sorting!")
    print("Program ini akan membandingkan waktu eksekusi Quicksort dan Mergesort")
    print("untuk berbagai ukuran input yang Anda tentukan.")
    print("\nContoh ukuran input yang bisa Anda masukkan: 100, 500, 1000, 5000, dst.")
    
    input_sizes = get_user_input()
    results = analyze_complexity(input_sizes)
    
    # Menampilkan hasil analisis dalam bentuk tabel
    print("\nHasil Analisis:")
    print("================================")
    print("Ukuran Input | Quicksort (s) | Mergesort (s)")
    print("--------------------------------")
    
    for i in range(len(results['input_sizes'])):
        print(f"{results['input_sizes'][i]:11d} | {results['quicksort_times'][i]:12.6f} | {results['mergesort_times'][i]:12.6f}")

if __name__ == "__main__":
    main()