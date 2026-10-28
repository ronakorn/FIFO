from pathlib import Path
root=Path('/home/user/fifo-wealth-os-web')
# FIRE calculator user-facing copy; tooltip implementation intentionally untouched.
p=root/'src/components/fire/FIRECalculator.tsx';s=p.read_text()
s=s.replace("import React, { useEffect, useMemo, useState } from 'react';", "import React, { useEffect, useMemo, useState } from 'react';\nimport { useTranslations } from 'next-intl';")
s=s.replace("}: FIRECalculatorProps) {\n  const {", "}: FIRECalculatorProps) {\n  const t = useTranslations('fire');\n  const {")
s=s.replace('Real-Time Decimal.js Engine', "{t('calculatorEngine')}")
s=s.replace('คำนวณเป้าหมาย FIRE ของคุณ', "{t('calculatorTitle')}")
s=s.replace('ปรับสมมติฐานค่าใช้จ่ายและอัตราถอนเงินปลอดภัยเพื่อดูเงินก้อนเป้าหมายทันที', "{t('calculatorDescription')}")
s=s.replace('เงินก้อนสู่อิสรภาพทางการเงิน (FIRE Number)', "{t('fireNumber')}")
s=s.replace('ถึงเป้าหมายในอีก ~{yearsToFIREStr} ปี (ปรับเงินเฟ้อจริง)', "{t('yearsToTarget', { years: yearsToFIREStr })}")
s=s.replace('พอร์ตจริงเชื่อมโยง: {formatTHB(livePortfolioValueTHB)}', "{t('linkedLivePortfolio', { amount: formatTHB(livePortfolioValueTHB) })}")
s=s.replace('ค่าใช้จ่ายหลังเกษียณ / เดือน (฿)', "{t('monthlyExpenses')}")
s=s.replace('อัตราถอน SWR (%)', "{t('withdrawalRate')}")
s=s.replace('เงินออมอื่นนอกพอร์ตปัจจุบัน (฿)', "{t('otherSavings')}")
s=s.replace('เงินลงทุนเพิ่มรายเดือน (DCA ฿)', "{t('monthlyContribution')}")
s=s.replace('ผลตอบแทน/ปี (%)', "{t('expectedReturn')}")
s=s.replace('เงินเฟ้อ/ปี (%)', "{t('inflation')}")
s=s.replace('ช่วงจำลอง (ปี)', "{t('simulationHorizon')}")
s=s.replace("? 'กำลังจำลองเส้นทาง GBM...'\n                : 'จำลอง Monte Carlo (150 เส้นทาง)'", "? t('simulateLoading')\n                : t('simulateMonteCarlo')")
s=s.replace('บันทึกเป้าหมาย', "{t('saveGoal')}")
p.write_text(s)

# Routes with static error messages. No logic changes.
p=root/'src/app/[locale]/loading.tsx';s=p.read_text()
# inspect/simple text wrapper conversion
if "useTranslations" not in s:
 s=s.replace("import", "import { getTranslations } from 'next-intl/server';\n\nimport",1)
 s=s.replace('export default function Loading()', 'export default async function Loading()')
 # inject translation at function start
 s=s.replace('{\n  return (', "{\n  const t = await getTranslations('appMessages');\n  return (")
s=s.replace('Loading FIFO Wealth OS…', "{t('loadingLabel')}")
s=s.replace('Private wealth management and Thai tax engine', "{t('loadingSubline')}")
p.write_text(s)

p=root/'src/app/[locale]/error.tsx';s=p.read_text()
if "useTranslations" not in s:
 # place next-intl import after use client
 lines=s.splitlines()
 idx=1 if lines and lines[0].strip()=="'use client';" else 0
 lines.insert(idx, "import { useTranslations } from 'next-intl';")
 s='\n'.join(lines)+'\n'
# hook in component body
s=s.replace('  const [errorId, setErrorId] = useState<string | null>(null);', "  const t = useTranslations('appMessages');\n  const [errorId, setErrorId] = useState<string | null>(null);")
s=s.replace('Something went wrong while loading this page', "{t('globalErrorTitle')}")
s=s.replace('This page could not be displayed. Please try again.', "{t('globalErrorMessage')}")
p.write_text(s)

# Pages: localize any route-level ErrorBoundary fallback title.
route_repls={
 'src/app/[locale]/gold/page.tsx':('goldPageError','GoldEngine'),
 'src/app/[locale]/multi-assets/page.tsx':('multiAssetPageError',None),
 'src/app/[locale]/fire/page.tsx':('firePageError','fire'),
 'src/app/[locale]/admin/audit-logs/page.tsx':('auditPageError','AuditTrail'),
 'src/app/[locale]/journal/page.tsx':('journalPageError','journal'),
}
for rel,(key,namespace) in route_repls.items():
 p=root/rel;s=p.read_text()
 if "'use client';" not in s and rel.endswith('/multi-assets/page.tsx'):
  s="'use client';\n\n"+s
 if "useTranslations" not in s:
  # insert with imports
  s=s.replace('import ', "import { useTranslations } from 'next-intl';\nimport ",1)
 # inject t inside the default function body, supporting common declaration patterns
 import re
 # get first function after export default
 m=re.search(r'(export default function\s+\w*\s*\([^)]*\)\s*\{)',s)
 if m:
  body=m.group(1)
  if namespace:
   inject=f"\n  const t = useTranslations('{namespace}');"
  else:
   inject="\n  const t = useTranslations('appMessages');"
  if inject.strip() not in s:
   s=s[:m.end()]+inject+s[m.end():]
 # fallbacks may use title prop or string child
 s=s.replace('title="Unable to load gold analysis"', f'title={{t(\'{key}\')}}')
 s=s.replace('title="Unable to load Multi-Asset workspace"', f'title={{t(\'{key}\')}}')
 s=s.replace('title="Unable to load FIRE planning"', f'title={{t(\'{key}\')}}')
 s=s.replace('title="Unable to load the audit trail"', f'title={{t(\'{key}\')}}')
 s=s.replace('title="Unable to load Wealth Journal"', f'title={{t(\'{key}\')}}')
 # try exact known alternate hardcoded error phrases from scan
 s=s.replace('title="ไม่สามารถโหลดข้อมูลทองคำได้"', f'title={{t(\'{key}\')}}')
 s=s.replace('title="ไม่สามารถโหลด Audit Trail ได้"', f'title={{t(\'{key}\')}}')
 p.write_text(s)

# Planning fallback is within an existing module using next-intl at the route.
p=root/'src/app/[locale]/planning/page.tsx';s=p.read_text()
# Use hook within page wrapper only if absent, route has two page components.
if "useTranslations" not in s:
 s=s.replace('import ', "import { useTranslations } from 'next-intl';\nimport ",1)
# Add t in the default page component and use translated title where present.
import re
m=re.search(r'(export default function\s+\w*\s*\([^)]*\)\s*\{)',s)
if m and 'const t = useTranslations' not in s:
 s=s[:m.end()]+"\n  const t = useTranslations('appMessages');"+s[m.end():]
s=s.replace('title="Unable to load tax planning"', "title={t('planningPageError')}")
s=s.replace('title="Unable to load planning"', "title={t('planningPageError')}")
p.write_text(s)
print('localized FIRE calculator and route-level copy')
