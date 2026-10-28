# Multi-Asset CDM Usage Guide

## วิธีใช้งาน Unified CDM

### 1. สร้างธุรกรรมใหม่

```typescript
import { MultiAssetTransaction, AssetClass } from '../types/multiAsset';

// ตัวอย่าง: ซื้อพันธบัตรรัฐบาล
const bondTransaction: MultiAssetTransaction = {
  id: 'tx-001',
  portfolioId: 'portfolio-123',
  date: '2024-10-01',
  symbol: 'BOND-TH-2025',
  assetClass: 'BOND',
  type: 'BUY',
  qty: 10,
  price: '100000.00',
  gross: '1000000.00',
  comm: '500.00',
  vat: '0.00',
  net: '1000500.00',
  originalCurrency: 'THB',
  originalNet: '1000500.00',
  fxRate: '1.00',
  netTHB: '1000500.00',
  exchange: 'OTC',
  createdAt: new Date(),
  
  // Bond Extension
  bondExtension: {
    couponRate: '0.0500', // 5%
    paymentFrequency: 'SEMI_ANNUAL',
    maturityDate: '2025-10-01',
    faceValue: '100000.00',
    accruedInterest: '0.00',
    yieldToMaturity: '0.0480',
    creditRating: 'AAA',
    issuer: 'รัฐบาลไทย',
  },
};
```

### 2. ตรวจสอบความถูกต้อง

```typescript
import { validateMultiAssetTransaction } from '../types/multiAsset';

const validation = validateMultiAssetTransaction(bondTransaction);
if (!validation.isValid) {
  console.error('Validation errors:', validation.errors);
}
```

### 3. เข้าถึง Extension Data

```typescript
if (transaction.assetClass === 'BOND' && transaction.bondExtension) {
  const couponRate = transaction.bondExtension.couponRate;
  const maturityDate = transaction.bondExtension.maturityDate;
  // ...
}
```

## กฎเหล็กในการขยาย CDM

1. ห้ามแก้ไข BaseTransaction - ถ้าต้องการฟิลด์ใหม่ ให้สร้าง Extension ใหม่
2. Extension ต้องเป็น Optional - ใช้ ? เพื่อให้สินทรัพย์อื่นไม่จำเป็นต้องมี
3. ใช้ Decimal String - ฟิลด์ทางการเงินทั้งหมดต้องเป็น string เพื่อใช้กับ decimal.js
4. เพิ่ม Asset Class ใน ASSET_CLASS_CONFIG - เมื่อเพิ่มสินทรัพย์ใหม่ ต้องอัปเดต Config
5. เขียน Unit Test - ทุก Extension ต้องมี Test ตรวจสอบความถูกต้อง

## ตัวอย่างการเพิ่มสินทรัพย์ใหม่

หากต้องการเพิ่มสินทรัพย์ใหม่ (เช่น 'CRYPTO_NFT'):

1. เพิ่มใน AssetClass type
2. สร้าง Interface NFTExtension
3. เพิ่มฟิลด์ nftExtension?: NFTExtension ใน MultiAssetTransaction
4. เพิ่ม Config ใน ASSET_CLASS_CONFIG
5. เขียน Test

---

เมื่อเสร็จแล้ว จะมี **Unified CDM Package** ที่สมบูรณ์แล้ว ประกอบด้วย:

1. ✅ **`src/types/multiAsset.ts`** - Core CDM + All Extensions
2. ✅ **`src/config/multiAssetRules.ts`** - Business Rules & Tax Regulations
3. ✅ **`docs/CDM_USAGE_GUIDE.md`** - คู่มือการใช้งาน
