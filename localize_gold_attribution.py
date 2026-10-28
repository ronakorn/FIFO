from pathlib import Path
import re
p=Path('/home/user/fifo-wealth-os-web/src/components/gold/GoldAttributionChart.tsx')
s=p.read_text()
# Remove locale-specific presentation fields from chart rows; render them from message keys.
for field in ['goldDriverLabelTH','goldDriverLabelEN','fxDriverLabelTH','fxDriverLabelEN']:
 s=re.sub(rf'^\s*{field}: string;\n','',s,flags=re.M)
s=s.replace('  isThai: boolean;\n','')
s=s.replace('  isThai,\n}: CustomBrinsonTooltipProps)', '}: CustomBrinsonTooltipProps)')
# Translation keys from numeric ratios preserve calculations and keep labels locale-independent.
insert="""
type GoldDriverTranslationKey = 'goldDriverRally' | 'goldDriverPullback' | 'goldDriverFlat';
type FxDriverTranslationKey = 'fxDriverWeakening' | 'fxDriverStrengthening' | 'fxDriverFlat';

function getGoldDriverTranslationKey(ratio: string): GoldDriverTranslationKey {
  const value = new ChartDecimal(ratio || '0');
  return value.gt(0) ? 'goldDriverRally' : value.lt(0) ? 'goldDriverPullback' : 'goldDriverFlat';
}

function getFxDriverTranslationKey(ratio: string): FxDriverTranslationKey {
  const value = new ChartDecimal(ratio || '0');
  return value.gt(0) ? 'fxDriverWeakening' : value.lt(0) ? 'fxDriverStrengthening' : 'fxDriverFlat';
}
"""
anchor='interface CustomTooltipPayloadEntry {'
s=s.replace(anchor,insert+'\n'+anchor)
# Brinson tooltip uses its own message hook.
s=s.replace('}: CustomBrinsonTooltipProps) {\n  if (!active', "}: CustomBrinsonTooltipProps) {\n  const t = useTranslations('GoldEngine');\n  if (!active")
s=s.replace("  const goldDriverText = isThai\n    ? row.goldDriverLabelTH\n    : row.goldDriverLabelEN;\n  const fxDriverText = isThai ? row.fxDriverLabelTH : row.fxDriverLabelEN;", "  const goldDriverText = t(getGoldDriverTranslationKey(row.rGoldRatio));\n  const fxDriverText = t(getFxDriverTranslationKey(row.rFxRatio));")
# Remove now-obsolete hardcoded label defaults and computed labels.
for line in [
"      goldDriverLabelTH: 'ทองโลกทรงตัว',\n", "      goldDriverLabelEN: 'World Gold Flat',\n", "      fxDriverLabelTH: 'ค่าเงินบาททรงตัว',\n", "      fxDriverLabelEN: 'THB Flat',\n",
]: s=s.replace(line,'')
s=re.sub(r"  const goldDriverLabelTH = rGold\.gt\(0\)[\s\S]*?  const fxDriverLabelEN = rFx\.gt\(0\)[\s\S]*?\n\n",'',s,count=1)
for line in [
"    goldDriverLabelTH,\n", "    goldDriverLabelEN,\n", "    fxDriverLabelTH,\n", "    fxDriverLabelEN,\n",
"    goldDriverLabelTH: item.goldDriverLabelTH,\n", "    goldDriverLabelEN: item.goldDriverLabelEN,\n", "    fxDriverLabelTH: item.fxDriverLabelTH,\n", "    fxDriverLabelEN: item.fxDriverLabelEN,\n",
]: s=s.replace(line,'')
# Localized tooltip text; math remains invariant.
s=s.replace("{row.mode === 'UNREALIZED' ? 'Unrealized G/L' : 'Realized G/L'}", "{row.mode === 'UNREALIZED' ? t('modeUnrealized') : t('modeRealized')}")
s=s.replace('Gold Alpha • {goldDriverText}', "{t('goldAlpha')} • {goldDriverText}")
s=s.replace('FX Impact • {fxDriverText}', "{t('fxImpact')} • {fxDriverText}")
s=s.replace('<span>Gold + FX === Total G/L</span>', "<span>{t('zeroResidualCheck')}</span>")
s=s.replace('          Residual: ฿{row.unexplainedResidualTHB}', "          {t('formulaResidual', { amount: row.unexplainedResidualTHB })}")
# Locale-aware main UI copy.
s=s.replace("{isThai ? 'สถานะถือครอง (Unrealized)' : 'Open (Unrealized)'}", "{t('modeUnrealized')}")
s=s.replace("{isThai ? 'ขายรับรู้จริง (Realized)' : 'Closed (Realized)'}", "{t('modeRealized')}")
s=s.replace('<strong>GTA Parity 96.5%</strong>', "<strong>{t('gtaParityFormula')}</strong>")
s=s.replace("{isThai ? 'สมาคมฯ' : 'GTA Quote'}", "{t('gtaQuote')}")
s=s.replace("{isThai ? 'กำไรจากทองโลกวิ่ง (Gold Alpha)' : 'World Gold Alpha'}", "{t('goldAlpha')}")
s=s.replace("{isThai ? 'ผลกระทบค่าเงิน (บาทอ่อน/แข็ง)' : 'USD/THB FX Impact'}", "{t('fxImpact')}")
s=s.replace("{isThai ? 'กำไร/ขาดทุนสุทธิรวม (Total G/L)' : 'Net Total G/L'}", "{t('totalGL')}")
s=s.replace('content={<BrinsonFormulaTooltip isThai={isThai} />}', 'content={<BrinsonFormulaTooltip />}')
s=s.replace("isThai\n                    ? 'กำไร/ขาดทุนจากทองโลก (Gold Alpha)'\n                    : 'World Gold Alpha (THB)'", "t('goldAlpha')")
s=s.replace("isThai\n                    ? 'ผลกระทบค่าเงินบาท (FX Impact)'\n                    : 'USD/THB FX Impact (THB)'", "t('fxImpact')")
s=s.replace("{isThai\n              ? 'ยังไม่มีรายการขายรับรู้กำไร/ขาดทุน (Realized G/L) ในพอร์ตนี้'\n              : 'No closed realized gold transactions in this portfolio yet.'}", "{t('noRealizedGoldTransactions')}")
s=s.replace('{isThai ? row.goldDriverLabelTH : row.goldDriverLabelEN}', '{t(getGoldDriverTranslationKey(row.rGoldRatio))}')
s=s.replace('{isThai ? row.fxDriverLabelTH : row.fxDriverLabelEN}', '{t(getFxDriverTranslationKey(row.rFxRatio))}')
s=s.replace('{inspectedRow.symbol} — Multiplicative Brinson Proof (Decimal precision: 40)', "{inspectedRow.symbol} — {t('brinsonProofTitle')}")
s=s.replace('Gold = {formatTHB(inspectedRow.costBasisTHB)}', "{t('goldFormulaLabel')} = {formatTHB(inspectedRow.costBasisTHB)}")
s=s.replace('FX = (Cost + Gold) × ({formatSignedRatio(inspectedRow.rFxRatio)})', "{t('fxImpactFormula')} = ({t('costBasisLabel')} + {t('goldAlpha')}) × ({formatSignedRatio(inspectedRow.rFxRatio)})")
s=s.replace('Total G/L: {formatSignedTHB(inspectedRow.totalGLTHB)} (Residual: ฿', "{t('totalGL')}: {formatSignedTHB(inspectedRow.totalGLTHB)} ({t('residual')}: ฿")
p.write_text(s)
print('localized gold attribution copy and removed row-embedded language fields')
