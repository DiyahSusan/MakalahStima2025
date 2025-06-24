import re
from collections import Counter, defaultdict

def kmp_search(text, pattern):
    
    def compute_lps(pattern):
        """Menghitung Longest Proper Prefix yang juga Suffix"""
        m = len(pattern)
        lps = [0] * m
        length = 0  
        i = 1
        
        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
    
    n = len(text)
    m = len(pattern)
    
    if m == 0:
        return []
    
    lps = compute_lps(pattern)
    
    matches = []
    i = 0  # index untuk text
    j = 0  # index untuk pattern
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return matches


def boyer_moore_search(text, pattern):
    
    def bad_char_table(pattern):
        """Membuat tabel bad character"""
        table = {}
        m = len(pattern)
        
        # Inisialisasi semua karakter dengan -1
        for i in range(m):
            table[pattern[i]] = -1
        
        # Isi tabel dengan posisi terakhir setiap karakter
        for i in range(m):
            table[pattern[i]] = i
        
        return table
    
    n = len(text)
    m = len(pattern)
    
    if m == 0:
        return []
    
    bad_char = bad_char_table(pattern)
    
    matches = []
    s = 0  
    
    while s <= n - m:
        j = m - 1
        
        # Cocokkan pattern dari kanan ke kiri
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        
        if j < 0:
            matches.append(s)
            s += (m - bad_char.get(text[s + m], -1) - 1) if s + m < n else 1
        else:
            char = text[s + j]
            shift = max(1, j - bad_char.get(char, -1))
            s += shift
    
    return matches


def regex_pattern_search(text, patterns, case_sensitive=True):
    
    results = {
        'pattern_counts': Counter(),
        'pattern_positions': defaultdict(list),
        'total_matches': 0,
        'total_word' : 0,
        'matched_text': defaultdict(list),
        'unique_matches': defaultdict(set)
    }
    
    # Flags untuk regex
    flags = 0 if case_sensitive else re.IGNORECASE
    words = text.split()

    # Hitung jumlah kata
    word_count = len(words)

    results['total_word'] = word_count

    if isinstance(patterns, list):
        pattern_dict = {f"pattern_{i+1}": pattern for i, pattern in enumerate(patterns)}
    else:
        pattern_dict = patterns
    
    for pattern_name, pattern in pattern_dict.items():
        try:
            # Cari semua kemunculan
            matches = list(re.finditer(pattern, text, flags))
            
            # Simpan hasil
            results['pattern_counts'][pattern_name] = len(matches)
            results['total_matches'] += len(matches)
            
            for match in matches:
                match_info = {
                    'start': match.start(),
                    'end': match.end(),
                    'matched_text': match.group(),
                    'groups': match.groups() if match.groups() else None
                }
                results['pattern_positions'][pattern_name].append(match_info)
                results['matched_text'][pattern_name].append(match.group())
                results['unique_matches'][pattern_name].add(match.group().lower())
                
        except re.error as e:
            print(f"Error in pattern '{pattern_name}': {pattern} - {e}")
            results['pattern_counts'][pattern_name] = 0
    
    return results

def main():
    text = input("Masukkan teks: ")
    
    # pola berdasarkan hasil survei
    my_patterns = {
        'cape_pattern': r'\bcape\.?\w*\b',      
        'lelah_pattern': r'\blelah\.?\w*\b',    
        'tidur_pattern' : r'\btidur\.?\w*\b',
        'nangis_pattern' : r'\bnangis\.?\w*\b',
        'bosan_pattern' : r'\bbosan\.?\w*\b',
        'gatau_pattern' : r'\bgatau\.?\w*\b',
        'stres_pattern' : r'\bstres\.?\w*\b',
        'tolong_pattern' : r'\btolong\.?\w*\b',
        'demot_pattern' : r'\bdemot\.?\w*\b',
        'gila_pattern' : r'\bgila\.?\w*\b',
        'jenuh_pattern' : r'\bjenuh\.?\w*\b',
        'mati_pattern' : r'\bmati\.?\w*\b',
        'meninggal_pattern' : r'\bmeninggal\.?\w*\b',
        'nyerah_pattern' : r'\bnyerah\.?\w*\b',
        'malas_pattern' : r'\bmalas\.?\w*\b',
        'tolong_pattern' : r'\btolong\.?\w*\b',
        'kasar_pattern': r'\b(fak|cuki)\.?\w*\b'
    }
    
    exit_flag = False
    while not exit_flag:
        #opsi pencarian kata atau perhitungan pattern
        print("\nOpsi menu: ")
        print("1. Perhitungan kemunculan kata negatif")
        print("2. Pencarian kata negatif")
        opsi = input("> ")
        if(opsi == '1'):
            print(f"\nTeks: {text}")
            results = regex_pattern_search(text, my_patterns, case_sensitive=False)
            # print(results) #debug
            print(f"\033[93mTotal kata: {results['total_word']}\033[0m")
            print(f"\033[93mTotal kecocokan: {results['total_matches']}\033[0m")
            print(f"\033[93mPersentase kemunculan: {results['total_matches'] / results['total_word'] * 100 if results['total_word'] > 0 else 0:.2f}%\033[0m")
        elif(opsi == '2'):
            print("\nAlgoritma pencarian")
            print("1. KMP Algorithm")
            print("2. Boyer-Moore Algorithm")
            algo = input("> ")
            keyword = input("Masukkan keyword pencarian: ")
            if(algo == '1'):
                matches = kmp_search(text, keyword)
            elif(algo == '2'):
                matches = boyer_moore_search(text, keyword)
            print(f"\033[93mPola ditemukan pada string di urutan {matches}\033[0m")

        user_input = input("Ketik 'exit' untuk keluar atau tekan Enter untuk lanjut: ")
        if user_input.strip().lower() == 'exit':
            exit_flag = True

main()



