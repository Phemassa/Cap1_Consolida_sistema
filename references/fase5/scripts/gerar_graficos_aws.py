#!/usr/bin/env python
"""
Script para gerar gráfico comparativo de custos AWS — São Paulo vs Virgínia

Gera PNG mostrando:
1. Custo mensal por região
2. Custo anual por região
3. Diferença percentual
"""

import matplotlib.pyplot as plt

# Dados de custos (em USD) extraídos dos prints da AWS Pricing Calculator
regions = ['São Paulo\n(sa-east-1)', 'Virgínia do Norte\n(us-east-1)']
custos_mensais = [43.07, 30.88]
custos_anuais = [516.84, 370.56]

# Configuração da figura
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Comparativo de Custos AWS — EC2 t3.micro (2 vCPU, 1 GiB RAM, 50 GB SSD)', 
             fontsize=16, fontweight='bold', y=0.98)

# ========== Gráfico 1: Custo Mensal ==========
ax1 = axes[0]
bars1 = ax1.bar(regions, custos_mensais, color=['#FF6B6B', '#4ECDC4'], width=0.6, edgecolor='black', linewidth=1.5)

# Adicionar valores nas barras
for i, bar in enumerate(bars1):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'US$ {height:.2f}',
             ha='center', va='bottom', fontsize=13, fontweight='bold')

ax1.set_ylabel('Custo (USD)', fontsize=12, fontweight='bold')
ax1.set_title('Custo Mensal', fontsize=13, fontweight='bold')
ax1.set_ylim(0, max(custos_mensais) * 1.2)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.set_axisbelow(True)

# Diferença percentual
diff_pct = ((custos_mensais[0] - custos_mensais[1]) / custos_mensais[1]) * 100
ax1.text(0.5, -0.25, f'Diferença: +{diff_pct:.1f}% (São Paulo é {diff_pct:.1f}% mais caro)',
         transform=ax1.transAxes, ha='center', fontsize=11, 
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# ========== Gráfico 2: Custo Anual ==========
ax2 = axes[1]
bars2 = ax2.bar(regions, custos_anuais, color=['#FF6B6B', '#4ECDC4'], width=0.6, edgecolor='black', linewidth=1.5)

# Adicionar valores nas barras
for i, bar in enumerate(bars2):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'US$ {height:.2f}',
             ha='center', va='bottom', fontsize=13, fontweight='bold')

ax2.set_ylabel('Custo (USD)', fontsize=12, fontweight='bold')
ax2.set_title('Custo Anual', fontsize=13, fontweight='bold')
ax2.set_ylim(0, max(custos_anuais) * 1.2)
ax2.grid(axis='y', alpha=0.3, linestyle='--')
ax2.set_axisbelow(True)

# Economia anual
economia = custos_anuais[0] - custos_anuais[1]
economia_pct = ((custos_anuais[0] - custos_anuais[1]) / custos_anuais[0]) * 100
ax2.text(0.5, -0.25, f'Economia (Virgínia): US$ {economia:.2f}/ano ({economia_pct:.1f}% menor)',
         transform=ax2.transAxes, ha='center', fontsize=11,
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

# Ajustar layout e salvar
plt.tight_layout()
plt.savefig('assets/comparativo_custos_aws.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Gráfico salvo em: assets/comparativo_custos_aws.png")

# Fechar figura
plt.close()

# ========== Gráfico 3: Tabela Comparativa ==========
fig, ax = plt.subplots(figsize=(12, 6))
ax.axis('tight')
ax.axis('off')

# Dados da tabela
table_data = [
    ['Critério', 'São Paulo (sa-east-1)', 'Virgínia do Norte (us-east-1)'],
    ['Custo mensal', 'US$ 43.07', 'US$ 30.88 (menor)'],
    ['Custo anual', 'US$ 516.84', 'US$ 370.56 (menor)'],
    ['Economia anual', '—', 'US$ 146.28 (28.3% menor)'],
    ['Latência para Brasil', '~5 ms (melhor)', '~130 ms (pior)'],
    ['Conformidade LGPD', 'Nativa', 'Requer análise adicional'],
    ['Soberania dos dados', 'Dados no Brasil', 'Dados no exterior'],
]

# Cores para linhas alternadas
colors = [['#E8E8E8'] * 3]  # Cabeçalho
for i in range(1, len(table_data)):
    if i % 2 == 0:
        colors.append(['#F5F5F5'] * 3)
    else:
        colors.append(['#FFFFFF'] * 3)

table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.25, 0.35, 0.35], cellColours=colors)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.5)

# Estilo do cabeçalho
for i in range(3):
    table[(0, i)].set_facecolor('#1976D2')
    table[(0, i)].set_text_props(weight='bold', color='white')

plt.title('Comparativo Detalhado — São Paulo vs Virgínia do Norte', 
          fontsize=14, fontweight='bold', pad=20)

plt.savefig('assets/tabela_comparativa_aws.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Tabela salva em: assets/tabela_comparativa_aws.png")

plt.close()

print("\n📊 Gráficos gerados com sucesso!")
print("   • assets/comparativo_custos_aws.png")
print("   • assets/tabela_comparativa_aws.png")
