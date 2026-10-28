from pathlib import Path
root=Path('/home/user/fifo-wealth-os-web/src')

def rep(path, pairs):
 p=root/path; s=p.read_text()
 for old,new in pairs:
  if old not in s: print('MISSING',path,repr(old[:70]))
  else: s=s.replace(old,new)
 p.write_text(s)

# Portfolio list route
p=root/'app/[locale]/portfolios/page.tsx';s=p.read_text()
s=s.replace("import React, { useState } from 'react';", "import React, { useState } from 'react';\nimport { useTranslations } from 'next-intl';")
s=s.replace("export default function PortfoliosPage() {", "export default function PortfoliosPage() {\n  const t = useTranslations('portfolioList');")
replacements=[
("setFormError('กรุณากรอกชื่อพอร์ตการลงทุน');","setFormError(t('formErrorName'))"),
("<ErrorBoundary fallbackTitle=\"ไม่สามารถแสดงรายการพอร์ตการลงทุนได้\">","<ErrorBoundary fallbackTitle={t('boundaryTitle')}>") ,
('>\n              Multi-Portfolio Management\n            </p>','>\n              {t(\'eyebrow\')}\n            </p>'),
('>\n              พอร์ตการลงทุนทั้งหมดของคุณ\n            </h1>','>\n              {t(\'title\')}\n            </h1>'),
('>\n              บริหารแยกพอร์ตตามกระดานเทรดหรือสกุลเงิน พร้อมคำนวณ FIFO แยกแต่ละพอร์ตอย่างอิสระ\n            </p>','>\n              {t(\'subtitle\')}\n            </p>'),
('🔄 Sync IBKR / นำเข้า CSV','{t(\'syncImport\')}'),
('                    สร้างพอร์ตใหม่','                    {t(\'createNew\')}'),
('<DialogTitle>สร้างพอร์ตการลงทุนใหม่</DialogTitle>','<DialogTitle>{t(\'dialogTitle\')}</DialogTitle>'),
('                      กำหนดชื่อพอร์ตและสกุลเงินหลัก (แนะนำ THB สำหรับยื่นภาษีกรมสรรพากร)','                      {t(\'dialogDescription\')}'),
('                        ชื่อพอร์ต','                        {t(\'nameLabel\')}'),
('placeholder="เช่น Bitkub Long-Term Crypto"','placeholder={t(\'namePlaceholder\')}'),
('                        สกุลเงินหลัก (Base Currency)','                        {t(\'currencyLabel\')}'),
('<option value="THB">THB - บาทไทย</option>','<option value="THB">{t(\'thbOption\')}</option>'),
('<option value="USD">USD - ดอลลาร์สหรัฐ</option>','<option value="USD">{t(\'usdOption\')}</option>'),
('                        ยกเลิก','                        {t(\'cancel\')}'),
("{createMutation.isPending ? 'กำลังบันทึก...' : 'สร้างพอร์ต'}","{createMutation.isPending ? t('saving') : t('create')}"),
('                เข้าสู่ระบบเพื่อสร้างพอร์ตจริง','                {t(\'loginToCreate\')}'),
('<LoadingSpinner label="กำลังโหลดพอร์ตการลงทุนของคุณ..." />','<LoadingSpinner label={t(\'loading\')} />'),
('message={extractApiErrorMessage(portfoliosQuery.error)}','message={extractApiErrorMessage(portfoliosQuery.error, t(\'loadError\'))}'),
]
for old,new in replacements:
 if old not in s: print('MISSING portfolios',repr(old[:80]))
 else:s=s.replace(old,new)
p.write_text(s)

# Portfolio card
p=root/'components/PortfolioCard.tsx';s=p.read_text()
s=s.replace("import React from 'react';\nimport Link from 'next/link';", "import React from 'react';\nimport { useLocale, useTranslations } from 'next-intl';\nimport { Link } from '@/navigation';")
s=s.replace("}: PortfolioCardProps) {\n  const summary", "}: PortfolioCardProps) {\n  const t = useTranslations('portfolioCard');\n  const locale = useLocale();\n  const summary")
for old,new in [
('''                สกุลเงินหลัก {portfolio.baseCurrency} • สร้างเมื่อ {formatDateShort(portfolio.createdAt)}''', '''                {t('baseCurrency')} {portfolio.baseCurrency} • {t('createdOn', { date: formatDateShort(portfolio.createdAt, locale === 'th' ? 'th-TH' : 'en-GB') })}'''),
('''              {txCount} รายการ''','''              {t('transactionCount', { count: txCount })}'''),
('''aria-label={`ลบพอร์ต ${portfolio.name}`}''','''aria-label={t('deletePortfolio', { name: portfolio.name })}'''),
('''              มูลค่าตลาดคงเหลือ (THB)''','''              {t('marketValue')}'''),
('''              กำไรที่รับรู้แล้ว (Realized)''','''              {t('realizedGL')}'''),
('''            นำเข้า CSV''','''            {t('csvImport')}'''),
('''            ภาษี {taxYear}''','''            {t('taxYear', { year: taxYear })}'''),
('''          เปิดพอร์ต''','''          {t('openPortfolio')}'''),
]:
 if old not in s: print('MISSING PortfolioCard',repr(old[:90]))
 else:s=s.replace(old,new)
p.write_text(s)

# Portfolio detail
p=root/'app/[locale]/portfolios/[id]/page.tsx';s=p.read_text()
s=s.replace("import Link from 'next/link';", "import { Link } from '@/navigation';\nimport { useTranslations } from 'next-intl';")
s=s.replace("export default function PortfolioDetailPage() {\n  const params", "export default function PortfolioDetailPage() {\n  const t = useTranslations('portfolioDetail');\n  const params")
replacements=[
('label="กำลังโหลดข้อมูลพอร์ตและคำนวณ FIFO Lots..."','label={t(\'loading\')}'),
('title="ไม่พบข้อมูลพอร์ตการลงทุน"','title={t(\'missingTitle\')}'),
('title="ไม่สามารถเปิดพอร์ตนี้ได้"','title={t(\'cannotOpenTitle\')}'),
('message="กรุณาเข้าสู่ระบบหรือเลือกพอร์ตการลงทุนที่ถูกต้อง"','message={t(\'loginOrChoose\')}'),
('<ErrorBoundary fallbackTitle="เกิดข้อผิดพลาดในหน้ารายละเอียดพอร์ต">','<ErrorBoundary fallbackTitle={t(\'boundaryTitle\')}>'),
('''              กลับไปหน้ารวมพอร์ต''','''              {t('back')}'''),
('''                Base: {portfolio.baseCurrency}''','''                {t('base', { currency: portfolio.baseCurrency })}'''),
('''              นำเข้า CSV เข้าพอร์ตนี้''','''              {t('importCsv')}'''),
('''              รายงานภาษีปี {selectedTaxYear}''','''              {t('taxReport', { year: selectedTaxYear })}'''),
('<span>มูลค่าตลาดคงเหลือ (THB)</span>','<span>{t(\'marketValue\')}</span>'),
('''              ต้นทุน FIFO คงเหลือ: {formatTHB(summary?.openCostBasisTHB ?? 0)}''','''              {t('openCostBasis', { amount: formatTHB(summary?.openCostBasisTHB ?? 0) })}'''),
('<span>กำไรที่รับรู้แล้ว (Realized G/L)</span>','<span>{t(\'realizedGL\')}</span>'),
('''              ยอดขายรวม: {formatTHB(summary?.totalProceeds ?? 0)}''','''              {t('totalSales', { amount: formatTHB(summary?.totalProceeds ?? 0) })}'''),
('<span>กำไรที่ยังไม่รับรู้ (Unrealized G/L)</span>','<span>{t(\'unrealizedGL\')}</span>'),
('''              จำนวนทั้งหมด {lots.length} FIFO Lots''','''              {t('lotCount', { count: lots.length })}'''),
('title="สัดส่วนสินทรัพย์ที่ถือครองในพอร์ต"','title={t(\'allocationTitle\')}'),
('subtitle="คำนวณจาก Open FIFO Lots (THB)"','subtitle={t(\'allocationSubtitle\')}'),
('''                <TabsTrigger value="lots">ตาราง FIFO Tax Lots ({lots.length})</TabsTrigger>''','''                <TabsTrigger value="lots">{t('lotsTab', { count: lots.length })}</TabsTrigger>'''),
('''                <TabsTrigger value="stats">สรุปต้นทุนการขาย</TabsTrigger>''','''                <TabsTrigger value="stats">{t('statsTab')}</TabsTrigger>'''),
('''                    ยังไม่มีรายการซื้อ (BUY) ในพอร์ตนี้ • อัปโหลดไฟล์ CSV เพื่อเริ่มต้นคำนวณ FIFO Lots''','''                    {t('emptyLots')}'''),
('<th className="px-3 py-2.5">สินทรัพย์</th>','<th className="px-3 py-2.5">{t(\'asset\')}</th>'),
('<th className="px-3 py-2.5">วันที่ซื้อ</th>','<th className="px-3 py-2.5">{t(\'buyDate\')}</th>'),
('<th className="px-3 py-2.5 text-right">ซื้อ / คงเหลือ</th>','<th className="px-3 py-2.5 text-right">{t(\'buyRemaining\')}</th>'),
('<th className="px-3 py-2.5 text-right">ต้นทุน/หน่วย (THB)</th>','<th className="px-3 py-2.5 text-right">{t(\'unitCost\')}</th>'),
('<th className="px-3 py-2.5 text-right">Realized G/L</th>','<th className="px-3 py-2.5 text-right">{t(\'realizedGL\')}</th>'),
('<th className="px-3 py-2.5 text-center">สถานะ</th>','<th className="px-3 py-2.5 text-center">{t(\'status\')}</th>'),
('''                              {lot.status}''','''                              {lot.status === 'Sold' ? t('statusSold') : lot.status === 'Partial' ? t('statusPartial') : t('statusHold')}'''),
('''                      ต้นทุนที่ถูกตัดขายแล้ว (Total Cost Sold)''','''                      {t('totalCostSold')}'''),
('''                      รายรับสุทธิจากการขาย (Total Proceeds)''','''                      {t('totalProceeds')}'''),
]
for old,new in replacements:
 if old not in s: print('MISSING portfolio detail',repr(old[:90]))
 else:s=s.replace(old,new)
p.write_text(s)

# Transaction table
p=root/'components/TransactionTable.tsx';s=p.read_text()
s=s.replace("import React, { useMemo, useState } from 'react';", "import React, { useMemo, useState } from 'react';\nimport { useLocale, useTranslations } from 'next-intl';")
s=s.replace("}: TransactionTableProps) {\n  const [search", "}: TransactionTableProps) {\n  const t = useTranslations('transactions');\n  const locale = useLocale();\n  const [search")
replacements=[
('''            สมุดบัญชีรายการซื้อขาย (Transaction Ledger)''','''            {t('title')}'''),
('''            รายการซื้อขายพร้อมอัตราแลกเปลี่ยนธนาคารแห่งประเทศไทย ณ วันเกิดธุรกรรม''','''            {t('subtitle')}'''),
('placeholder="ค้นหาสินทรัพย์ (เช่น AAPL, BTC)..."','placeholder={t(\'searchPlaceholder\')}'),
('aria-label="กรองตามประเภทธุรกรรม"','aria-label={t(\'filterLabel\')}'),
('<option value="ALL">ทุกธุรกรรม (BUY / SELL / FEE)</option>','<option value="ALL">{t(\'allTypes\')}</option>'),
('<option value="BUY">เฉพาะซื้อ (BUY)</option>','<option value="BUY">{t(\'buyOnly\')}</option>'),
('<option value="SELL">เฉพาะขาย (SELL)</option>','<option value="SELL">{t(\'sellOnly\')}</option>'),
('<option value="FEE">ค่าธรรมเนียม Gas (FEE)</option>','<option value="FEE">{t(\'feeOnly\')}</option>'),
('''            {sortDesc ? 'ล่าสุดก่อน' : 'เก่าสุดก่อน'}''','''            {sortDesc ? t('sortNewest') : t('sortOldest')}'''),
('<th className="px-4 py-2.5">วันที่</th>','<th className="px-4 py-2.5">{t(\'date\')}</th>'),
('<th className="px-4 py-2.5">ฝั่ง</th>','<th className="px-4 py-2.5">{t(\'side\')}</th>'),
('<th className="px-4 py-2.5">สินทรัพย์</th>','<th className="px-4 py-2.5">{t(\'asset\')}</th>'),
('<th className="px-4 py-2.5 text-right">จำนวน</th>','<th className="px-4 py-2.5 text-right">{t(\'quantity\')}</th>'),
('<th className="px-4 py-2.5 text-right">ราคาต่อหน่วย</th>','<th className="px-4 py-2.5 text-right">{t(\'unitPrice\')}</th>'),
('<th className="px-4 py-2.5 text-right">ค่าธรรมเนียม</th>','<th className="px-4 py-2.5 text-right">{t(\'fee\')}</th>'),
('<th className="px-4 py-2.5 text-right">FX Rate</th>','<th className="px-4 py-2.5 text-right">{t(\'fxRate\')}</th>'),
('<th className="px-4 py-2.5 text-right">ยอดสุทธิ (THB)</th>','<th className="px-4 py-2.5 text-right">{t(\'netTHB\')}</th>'),
('''                  ไม่พบรายการธุรกรรมที่ตรงกับเงื่อนไขการค้นหา''','''                  {t('noResults')}'''),
('{formatDateShort(tx.date)}',"{formatDateShort(tx.date, locale === 'th' ? 'th-TH' : 'en-GB')}"),
('''                        {rawType}''','''                        {rawType === 'BUY' ? t('buy') : rawType === 'SELL' ? t('sell') : t('feeType')}'''),
]
for old,new in replacements:
 if old not in s: print('MISSING transactions',repr(old[:90]))
 else:s=s.replace(old,new)
s=s.replace('''            type="button"
            onClick={() => setSortDesc((s) => !s)}''','''            type="button"
            aria-label={t('sortLabel')}
            onClick={() => setSortDesc((s) => !s)}''')
p.write_text(s)

# Tax page
p=root/'app/[locale]/tax/[portfolioId]/[year]/page.tsx';s=p.read_text()
s=s.replace("import { useParams, useRouter } from 'next/navigation';", "import { useParams } from 'next/navigation';\nimport { useRouter } from '@/navigation';\nimport { useTranslations } from 'next-intl';")
s=s.replace("export default function TaxReportPage() {\n  const params", "export default function TaxReportPage() {\n  const t = useTranslations('tax.page');\n  const params")
for old,new in [
('<ErrorBoundary fallbackTitle="ไม่สามารถแสดงผลรายงานภาษีได้">','<ErrorBoundary fallbackTitle={t(\'boundaryTitle\')}>'),
('<span>เลือกพอร์ต:</span>','<span>{t(\'portfolioLabel\')}</span>'),
('aria-label="เลือกพอร์ตสำหรับคำนวณภาษี"','aria-label={t(\'portfolioAria\')}'),
('<span className="text-xs font-semibold text-gray-500 dark:text-gray-400">ปีภาษี:</span>','<span className="text-xs font-semibold text-gray-500 dark:text-gray-400">{t(\'yearLabel\')}</span>'),
('label={`กำลังคำนวณภาษีประจำปี ${parsedYear} ตามประมวลรัษฎากร...`}','label={t(\'loading\', { year: parsedYear })}'),
('title="ไม่สามารถดึงสรุปภาษีจาก Backend"','title={t(\'errorTitle\')}'),
('message={extractApiErrorMessage(taxQuery.error)}','message={extractApiErrorMessage(taxQuery.error, t(\'errorFallback\'))}'),
]:
 if old not in s: print('MISSING tax page',repr(old[:80]))
 else:s=s.replace(old,new)
p.write_text(s)

# Localized date helper
p=root/'lib/utils.ts';s=p.read_text()
s=s.replace("export function formatDateShort(isoDate: string): string {", "export function formatDateShort(isoDate: string, locale = 'en-GB'): string {")
s=s.replace("return new Intl.DateTimeFormat('en-GB', {", "return new Intl.DateTimeFormat(locale, {",1)
p.write_text(s)
