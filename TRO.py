import pulp
import pandas as pd

# --- A. DEFENISI DATA ---

# 1. List Gudang dan Toko
Gudang = ['G1', 'G2']
Toko = ['TA', 'TB', 'TC']

# 2. Biaya Transportasi per unit (Cost)
# Urutan: G1 ke [TA, TB, TC], G2 ke [TA, TB, TC]
biaya = {
    'G1': {'TA': 7, 'TB': 5, 'TC': 9},
    'G2': {'TA': 8, 'TB': 6, 'TC': 4}
}

# 3. Kapasitas Gudang (Supply)
kapasitas = {
    'G1': 150,
    'G2': 200
}

# 4. Permintaan Toko (Demand)
permintaan = {
    'TA': 100,
    'TB': 120,
    'TC': 130
}

# --- B. FORMULASI MODEL (LP) ---

# 1. Buat Objek Model
model = pulp.LpProblem("Model_Transportasi_PT_Maju_Jaya", pulp.LpMinimize)

# 2. Variabel Keputusan (X_ij)
# X_ij adalah jumlah unit yang dikirim dari Gudang i ke Toko j, harus non-negatif
x = pulp.LpVariable.dicts("X", [(i, j) for i in Gudang for j in Toko], lowBound=0, cat='Integer')

# 3. Fungsi Tujuan: Minimasi Biaya Total
# Z = SUM(C_ij * X_ij)
model += pulp.lpSum(biaya[i][j] * x[(i, j)] for i in Gudang for j in Toko), "Biaya_Total"

# 4. Kendala 1: Kapasitas Gudang (Supply)
for i in Gudang:
    model += pulp.lpSum(x[(i, j)] for j in Toko) <= kapasitas[i], f"Kapasitas_Gudang_{i}"

# 5. Kendala 2: Permintaan Toko (Demand)
for j in Toko:
    model += pulp.lpSum(x[(i, j)] for i in Gudang) == permintaan[j], f"Permintaan_Toko_{j}"


# --- C. SOLUSI ---

# 1. Pecahkan Model
model.solve()

# 2. Cek Status Solusi
print(f"Status Solusi: {pulp.LpStatus[model.status]}")

# 3. Tampilkan Biaya Total Optimal
biaya_optimal = pulp.value(model.objective)
print(f"Biaya Transportasi Minimum (Z_min): Rp {biaya_optimal:,.0f}")

# 4. Tampilkan Alokasi Optimal
alokasi_optimal = {}
for i in Gudang:
    alokasi_optimal[i] = {}
    for j in Toko:
        if x[(i, j)].varValue > 0:
            alokasi_optimal[i][j] = x[(i, j)].varValue

df_alokasi = pd.DataFrame(alokasi_optimal).fillna(0).T.astype(int)
print("\nMatriks Alokasi Optimal:")
print(df_alokasi)