from pathlib import Path
root=Path('/home/user/fifo-wealth-os-web')
# Error message shared UI.
p=root/'src/components/ErrorMessage.tsx';s=p.read_text()
s=s.replace("import React from 'react';", "import React from 'react';\nimport { useTranslations } from 'next-intl';")
s=s.replace("  title = 'เกิดข้อผิดพลาดในการโหลดข้อมูล',", "  title,")
s=s.replace('}: ErrorMessageProps) {\n  return (', "}: ErrorMessageProps) {\n  const t = useTranslations('common');\n  const resolvedTitle = title ?? t('errorTitle');\n  return (")
s=s.replace('{title}</h3>', '{resolvedTitle}</h3>')
s=s.replace('ลองใหม่อีกครั้ง', "{t('retry')}")
p.write_text(s)
# Generic Radix dialog close button.
p=root/'src/components/ui/dialog.tsx';s=p.read_text()
s=s.replace("import { X } from 'lucide-react';", "import { X } from 'lucide-react';\nimport { useTranslations } from 'next-intl';")
s=s.replace('>(({ className, children, ...props }, ref) => (\n  <DialogPortal>', ">(({ className, children, ...props }, ref) => {\n  const t = useTranslations('common');\n  return (\n  <DialogPortal>")
s=s.replace('aria-label="Close"', "aria-label={t('close')}")
s=s.replace('  </DialogPortal>\n));\nDialogContent.displayName', '  </DialogPortal>\n  );\n});\nDialogContent.displayName')
p.write_text(s)
# Advanced-assets bespoke modal.
p=root/'src/components/advancedAssets/ui.tsx';s=p.read_text()
s=s.replace("import React from 'react';", "import React from 'react';\nimport { useTranslations } from 'next-intl';")
s=s.replace('}: {\n  title: string;\n  description?: string;\n  onClose: () => void;\n  children: React.ReactNode;\n}) {\n  return (', "}: {\n  title: string;\n  description?: string;\n  onClose: () => void;\n  children: React.ReactNode;\n}) {\n  const t = useTranslations('common');\n  return (")
s=s.replace('aria-label="Close"', "aria-label={t('close')}")
p.write_text(s)
# Transaction table pagination.
p=root/'src/components/TransactionTable.tsx';s=p.read_text()
s=s.replace('แสดง {paginated.length} จากทั้งหมด {filtered.length} รายการ', "{t('showingCount', { current: paginated.length, total: filtered.length })}")
s=s.replace('            ก่อนหน้า\n', "            {t('previous')}\n")
s=s.replace('            หน้า {currentPage} / {totalPages}', "            {t('pageIndicator', { page: currentPage, total: totalPages })}")
s=s.replace('            ถัดไป\n', "            {t('next')}\n")
p.write_text(s)
# Chart defaults / loading labels. Preserve existing Recharts tooltips.
p=root/'src/components/Chart.tsx';s=p.read_text()
s=s.replace("import { useTheme } from 'next-themes';", "import { useTheme } from 'next-themes';\nimport { useTranslations } from 'next-intl';")
s=s.replace("  title = 'แนวโน้มมูลค่าพอร์ตรวมเทียบต้นทุน FIFO (THB)',\n  subtitle = 'Net Worth vs Open Cost Basis',", "  title,\n  subtitle,")
s=s.replace('  const [mounted, setMounted] = useState(false);\n  const { resolvedTheme } = useTheme();', "  const t = useTranslations('portfolioDetail');\n  const resolvedTitle = title ?? t('performanceChartTitle');\n  const resolvedSubtitle = subtitle ?? t('performanceChartSubtitle');\n  const [mounted, setMounted] = useState(false);\n  const { resolvedTheme } = useTheme();",1)
s=s.replace('{title}\n          </h3>\n          <p className="text-xs text-gray-500 dark:text-gray-400">{subtitle}</p>', '{resolvedTitle}\n          </h3>\n          <p className="text-xs text-gray-500 dark:text-gray-400">{resolvedSubtitle}</p>',1)
s=s.replace('กำลังโหลดกราฟ...', "{t('chartLoading')}")
s=s.replace("  title = 'สัดส่วนสินทรัพย์ที่ถือครองในพอร์ต',\n  subtitle = 'คำนวณจาก Open FIFO Lots (THB)',", "  title,\n  subtitle,")
# Add hook in pie component specifically.
marker='export function AssetAllocationPieChart({\n  data,\n  title,\n  subtitle,\n}: {\n  data: AllocationSlice[];\n  title?: string;\n  subtitle?: string;\n}) {\n'
if marker not in s:
 marker='export function AssetAllocationPieChart({\n  data,\n  title,\n  subtitle,\n}: {\n  data: AllocationSlice[];\n  title?: string;\n  subtitle?: string;\n}) {\n'
# If actual signature remains but defaults removed, add translations at start after opening function.
if marker in s:
 s=s.replace(marker,marker+"  const t = useTranslations('portfolioDetail');\n  const resolvedTitle = title ?? t('allocationTitle');\n  const resolvedSubtitle = subtitle ?? t('allocationSubtitle');\n",1)
else:
 s=s.replace('export function AssetAllocationPieChart({', 'export function AssetAllocationPieChart({')
 # fallback generic insert after function's props close
 pos=s.index('export function AssetAllocationPieChart')
 brace=s.index('  const [mounted',pos)
 s=s[:brace]+"  const t = useTranslations('portfolioDetail');\n  const resolvedTitle = title ?? t('allocationTitle');\n  const resolvedSubtitle = subtitle ?? t('allocationSubtitle');\n"+s[brace:]
s=s.replace('{title}\n        </h3>\n        <p className="text-xs text-gray-500 dark:text-gray-400">{subtitle}</p>', '{resolvedTitle}\n        </h3>\n        <p className="text-xs text-gray-500 dark:text-gray-400">{resolvedSubtitle}</p>',1)
s=s.replace('กำลังโหลดสัดส่วนพอร์ต...', "{t('allocationLoading')}")
s=s.replace('อัปโหลดไฟล์ CSV เพื่อดูสัดส่วนสินทรัพย์แบบเรียลไทม์', "{t('allocationEmpty')}")
p.write_text(s)
# AI drawer UI labels and localized fallback messages.
p=root/'src/components/ai/AIChatDrawer.tsx';s=p.read_text()
s=s.replace("      const fallbackReply =\n        locale === 'th'\n          ? `จากข้อมูลตัวอย่างในพอร์ตของคุณ เดือนที่ทำกำไรสูงสุดคือ **2024-10** ด้วยกำไรรับรู้จริง **฿11,470.65** และมูลค่าทรัพย์สินสุทธิรวม **฿231,169.89** (XIRR **18.45%**, Sharpe Ratio **1.55**)`\n          : `From your preview portfolio, your most profitable month was **2024-10** with **฿11,470.65** in realized gains and **฿231,169.89** total Net Worth (XIRR **18.45%**, Sharpe **1.55**).`;", "      const fallbackReply = t('previewFallback');")
s=s.replace("      const errText =\n        locale === 'th'\n          ? 'ขออภัย ไม่สามารถเชื่อมต่อระบบวิเคราะห์พอร์ตได้ในขณะนี้ กรุณาลองใหม่อีกครั้ง'\n          : 'Unable to reach the analytics engine right now. Please try again.';", "      const errText = t('errorFallback');")
s=s.replace('aria-label="Close AI assistant"', "aria-label={t('closeAssistant')}")
s=s.replace('aria-label="Close AI Drawer"', "aria-label={t('closeAssistant')}")
p.write_text(s)
# Family invite modal title/tag and close accessibility label.
p=root/'src/components/family/InviteModal.tsx';s=p.read_text()
s=s.replace('Privacy-First Household Sharing', "{t('privacyFirstSharing')}")
s=s.replace('                onClick={onClose}\n                className="rounded-xl p-1.5', "                onClick={onClose}\n                aria-label={t('closeInviteModal')}\n                className=\"rounded-xl p-1.5")
p.write_text(s)
print('patched shared components')
