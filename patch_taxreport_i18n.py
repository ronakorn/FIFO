from pathlib import Path
p=Path('/home/user/fifo-wealth-os-web/src/components/TaxReportViewer.tsx');s=p.read_text()
s=s.replace("import React, { useState } from 'react';", "import React, { useState } from 'react';\nimport { useLocale, useTranslations } from 'next-intl';")
start=s.index('const THAI_PIT_BRACKETS = [')
end=s.index('\n];',start)+3
s=s[:start]+'''const THAI_PIT_BRACKETS = [
  { key: 'exempt', min: 0, max: 150_000, rate: '0%', maxTax: 0, isExempt: true },
  { key: 'five', min: 150_001, max: 300_000, rate: '5%', maxTax: 7_500 },
  { key: 'ten', min: 300_001, max: 500_000, rate: '10%', maxTax: 20_000 },
  { key: 'fifteen', min: 500_001, max: 750_000, rate: '15%', maxTax: 37_500 },
  { key: 'twenty', min: 750_001, max: 1_000_000, rate: '20%', maxTax: 50_000 },
  { key: 'twentyFive', min: 1_000_001, max: 2_000_000, rate: '25%', maxTax: 250_000 },
  { key: 'thirty', min: 2_000_001, max: 5_000_000, rate: '30%', maxTax: 900_000 },
  { key: 'thirtyFive', min: 5_000_001, max: null, rate: '35%', maxTax: null },
] as const;'''+s[end:]
s=s.replace("  portfolioName = 'Multi-Asset Portfolio',", "  portfolioName,")
s=s.replace("}: TaxReportViewerProps) {\n  const [downloading", "}: TaxReportViewerProps) {\n  const t = useTranslations('taxReport');\n  const locale = useLocale();\n  const numberLocale = locale === 'th' ? 'th-TH' : 'en-US';\n  const formatTaxNumber = (value: number) => new Intl.NumberFormat(numberLocale).format(value);\n  const [downloading")
pairs=[
("'กรุณาเข้าสู่ระบบด้วยบัญชี Demo เพื่อดาวน์โหลดรายงาน PDF 5 หน้าจริงจาก Backend Engine'", "t('mockDownloadError')"),
("extractApiErrorMessage(err, 'ไม่สามารถสร้างไฟล์ PDF รายงานภาษีได้')", "extractApiErrorMessage(err, t('pdfErrorFallback'))"),
('''              Thai Revenue Department Compliance • ภ.ง.ด. 90 / 91''','''              {t('complianceBadge')}'''),
('''              รายงานสรุปภาษีเงินได้ประจำปี พ.ศ. {report.taxYear + 543} ({report.taxYear})''','''              {t('title', { beYear: report.taxYear + 543, ceYear: report.taxYear })}'''),
('''              พอร์ตการลงทุน:{' '}''','''              {t('portfolioLabel')}{' '}'''),
('''              • คำนวณต้นทุนด้วยวิธีเข้าก่อน-ออกก่อน (FIFO) และปัดเศษทศนิยม 2 ตำแหน่ง (ROUND_HALF_UP)''','''              • {t('fifoMethod')}'''),
('''                  กำลังสร้างเอกสาร PDF 5 หน้า...''','''                  {t('downloading')}'''),
('''                  ดาวน์โหลด PDF 5 หน้า (ภ.ง.ด. 90/91)''','''                  {t('download')}'''),
('''            สร้างและดาวน์โหลดรายงานภาษี PDF 5 หน้า (ฟอนต์ Sarabun มาตรฐานราชการ) สำเร็จแล้ว''','''            {t('downloadSuccess')}'''),
('<ErrorMessage title="แจ้งเตือนการดาวน์โหลด PDF" message={pdfError} />','<ErrorMessage title={t(\'downloadErrorTitle\')} message={pdfError} />'),
('<span>เงินได้พึงประเมินสุทธิรวม</span>','<span>{t(\'taxableIncome\')}</span>'),
('''            Capital Gains: {formatTHB(totalCapGainsTHB)} • ปันผล: {formatTHB(totalDivGrossTHB)}''','''            {t('capitalGains')}: {formatTHB(totalCapGainsTHB)} • {t('dividends')}: {formatTHB(totalDivGrossTHB)}'''),
('<span>เครดิตภาษีหัก ณ ที่จ่าย (WHT)</span>','<span>{t(\'withholdingCredit\')}</span>'),
('''            หัก ณ ที่จ่ายสะสมจากเงินปันผล ({report.dividends.length} รายการ)''','''            {t('withholdingFromDividends', { count: report.dividends.length })}'''),
("{taxPayableNum < 0 ? 'เครดิตภาษีชำระเกิน' : 'ภาษีที่ต้องชำระสุทธิ'}", "{taxPayableNum < 0 ? t('overpaidCredit') : t('netTaxPayable')}"),
("? 'ได้รับยกเว้น 150,000 บาทแรก (0%) พร้อมเครดิต WHT'\n              : 'คำนวณตามขั้นบันไดอัตราก้าวหน้า 0% - 35%'", "? t('taxExemptNote')\n              : t('progressiveTaxNote')"),
('<span>รายการทางภาษีทั้งหมด</span>','<span>{t(\'taxItems\')}</span>'),
('''            {report.capitalGains.length + report.dividends.length} รายการ''','''            {t('itemCount', { count: report.capitalGains.length + report.dividends.length })}'''),
('''            ขายสินทรัพย์ {report.capitalGains.length} • เงินปันผล {report.dividends.length}''','''            {t('capitalGainCount', { count: report.capitalGains.length, dividends: report.dividends.length })}'''),
('''              กำไรจากการขายสินทรัพย์ ({report.capitalGains.length})''','''              {t('capitalGainsTab', { count: report.capitalGains.length })}'''),
('''              เงินปันผล & ภาษีหัก ณ ที่จ่าย ({report.dividends.length})''','''              {t('dividendsTab', { count: report.dividends.length })}'''),
('''              อัตราภาษีเงินได้บุคคลธรรมดา (0% - 35%)''','''              {t('bracketsTab')}'''),
('''                ไม่มีรายการขายสินทรัพย์ (SELL) ที่ก่อให้เกิดกำไร/ขาดทุนในปีภาษี {report.taxYear}''','''                {t('noCapitalGains', { year: report.taxYear })}'''),
('<th className="px-4 py-2.5">วันที่ขาย</th>','<th className="px-4 py-2.5">{t(\'saleDate\')}</th>'),
('<th className="px-4 py-2.5">สินทรัพย์</th>','<th className="px-4 py-2.5">{t(\'security\')}</th>'),
('<th className="px-4 py-2.5 text-right">กำไรสุทธิ FIFO (THB)</th>','<th className="px-4 py-2.5 text-right">{t(\'fifoNetGain\')}</th>'),
('<th className="px-4 py-2.5 text-right">เงินได้พึงประเมิน (THB)</th>','<th className="px-4 py-2.5 text-right">{t(\'taxableIncomeTHB\')}</th>'),
('<th className="px-4 py-2.5 text-right">ภาษีหัก ณ ที่จ่าย</th>','<th className="px-4 py-2.5 text-right">{t(\'withholdingTax\')}</th>'),
('<th className="px-4 py-2.5 text-center">มาตราประมวลรัษฎากร</th>','<th className="px-4 py-2.5 text-center">{t(\'revenueCode\')}</th>'),
("{formatDateShort(ev.date)}", "{formatDateShort(ev.date, numberLocale)}"),
("{isTaxable ? 'มาตรา 40(4) พึงประเมิน' : 'ได้รับยกเว้น / ขาดทุน'}", "{isTaxable ? t('taxableSection') : t('exemptOrLoss')}"),
('''                ไม่มีรายการเงินปันผลในปีภาษี {report.taxYear}''','''                {t('noDividends', { year: report.taxYear })}'''),
('<th className="px-4 py-2.5">วันที่รับปันผล</th>','<th className="px-4 py-2.5">{t(\'dividendDate\')}</th>'),
('<th className="px-4 py-2.5">หลักทรัพย์</th>','<th className="px-4 py-2.5">{t(\'security\')}</th>'),
('<th className="px-4 py-2.5 text-right">เงินปันผลรับรวม (Gross THB)</th>','<th className="px-4 py-2.5 text-right">{t(\'grossDividends\')}</th>'),
('<th className="px-4 py-2.5 text-right">ภาษีหัก ณ ที่จ่าย (WHT THB)</th>','<th className="px-4 py-2.5 text-right">{t(\'withholdingTHB\')}</th>'),
('<th className="px-4 py-2.5 text-right">เงินได้พึงประเมิน (Taxable THB)</th>','<th className="px-4 py-2.5 text-right">{t(\'taxableTHB\')}</th>'),
('<th className="px-4 py-2.5">ช่วงเงินได้สุทธิต่อปี (บาท)</th>','<th className="px-4 py-2.5">{t(\'annualTaxableRange\')}</th>'),
('<th className="px-4 py-2.5">อัตราภาษี</th>','<th className="px-4 py-2.5">{t(\'taxRate\')}</th>'),
('<th className="px-4 py-2.5 text-right">ภาษีสูงสุดในขั้น</th>','<th className="px-4 py-2.5 text-right">{t(\'maxTaxInBracket\')}</th>'),
('''                      key={row.range}''','''                      key={row.key}'''),
('''                        {row.range}''','''                        {row.max === null ? t('aboveAmount', { amount: formatTaxNumber(row.min) }) : t('bracketRange', { min: formatTaxNumber(row.min), max: formatTaxNumber(row.max) })}'''),
('''                        {row.rate}''','''                        {row.rate}{row.isExempt ? ` (${t('exempt')})` : ''}'''),
('''                        {row.maxTax}''','''                        {row.maxTax === null ? t('basedOnExcess') : formatTHB(row.maxTax)}'''),
]
for old,new in pairs:
 if old not in s: print('MISS taxreport',repr(old[:100]))
 else:s=s.replace(old,new)
p.write_text(s)
