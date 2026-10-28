# Thai Local Broker Integration Hub — Partner Brief

**วันที่จัดทำ:** 27 ตุลาคม 2026  
**วัตถุประสงค์:** เอกสารประกอบการนำเสนอแนวคิด Sponsorship / Partnership สำหรับ Bitkub, Dime! และ Settrade Streaming

## แนวคิดผลิตภัณฑ์

ศูนย์กลางเชื่อมต่อประวัติการลงทุนจากโบรกเกอร์ไทยและสินทรัพย์ดิจิทัล โดยออกแบบให้ทำงานแบบ **Read-Only** เพื่อรวบรวมประวัติซื้อขายและเงินปันผลเข้าสู่พอร์ต FIFO และระบบวิเคราะห์ของ FIFO Wealth OS ผ่านประสบการณ์ผู้ใช้รูปแบบ Native Integration

หน้า Hub แสดงแบรนด์ทั้งสาม, สถานะการเชื่อมต่อ, Sync Now, เวลาซิงค์ล่าสุด, จำนวนรายการ, หน้าขอความยินยอมข้อมูลส่วนบุคคล และการยกเลิกพร้อมลบข้อมูลที่นำเข้าจาก Connector

## สถานะ Adapter และขอบเขตของ Demo

| ผู้ให้บริการ | Adapter / UX | สิ่งที่ทำงานในโค้ดชุดนี้ | สิ่งที่ต้องได้รับจาก Partner ก่อนใช้งานจริง |
|---|---|---|---|
| **Bitkub** | `BitkubReadOnlyAdapter` | โครงสร้าง API v3 HMAC, เรียกเฉพาะ GET สำหรับรายการซื้อขาย, แบ่งหน้าและแปลง BUY/SELL เป็น CDM; มี deterministic sandbox feed สำหรับ Demo | Read-Only API key/scope ที่ตรวจสอบกับ Bitkub แล้ว, endpoint/configuration สำหรับ production, rate-limit และแนวทาง backfill |
| **Dime!** | `DimeOpenApiAdapter` | โครงสร้าง OAuth/Open API + statement fallback, รองรับหุ้น US แบบ fractional, หุ้นไทย, ปันผล และ FX ผ่าน Decimal; feed ปัจจุบันเป็นตัวอย่าง sandbox | Partner API/OAuth, scope ที่อนุมัติ, sandbox และเอกสาร statement/schema ที่เป็นทางการ |
| **Streaming (SET)** | `StreamingPartnerModule` | UX แบบ Native สำหรับ Secure Statement Automation, parser ของ confirmation/dividend rows และข้อความ roadmap: “รองรับการเชื่อมต่ออัตโนมัติในอนาคตเมื่อตลาดหลักทรัพย์ฯ เปิด Open API”; feed ปัจจุบันเป็นตัวอย่าง sandbox | รูปแบบ statement ที่อนุมัติ, ช่องทางรับไฟล์/ยืนยันตัวตนจากบริษัทสมาชิกหรือ Settrade และการอนุมัติการเชื่อมต่อ |

> **ความโปร่งใสของ Demo:** หน้าจอจะแสดง `Sandbox Demo` อย่างชัดเจนเมื่อซิงค์ข้อมูลตัวอย่าง ไม่แสดงว่าเชื่อมต่อกับระบบ Partner จริง ส่วน Bitkub จะเลือก live adapter เมื่อกำหนด `BITKUB_PARTNER_API_URL`; Dime! และ Streaming ยังเป็น integration scaffolds/sandbox จนกว่าจะได้รับช่องทาง Partner ที่อนุมัติ

## Security, PDPA และการควบคุมข้อมูล

- **Read-Only by design:** ไม่มีฟังก์ชันส่งคำสั่งซื้อขาย ยกเลิกคำสั่ง หรือถอนสินทรัพย์ใน Thai Broker Adapter; ใน Production ต้องให้ Partner ยืนยัน scope ของ credential จริง ไม่ถือว่าคำประกาศ scope จาก UI เป็นการตรวจสอบสิทธิ์จาก Partner
- **AES-256-GCM:** เข้ารหัส API Key/Secret/Token ก่อนบันทึกลงฐานข้อมูล โดย runtime ต้องตั้ง `ENCRYPTION_KEY` ความยาวอย่างน้อย 32 ตัวอักษร; service ของ Thai Broker ปฏิเสธการเชื่อมต่อหากไม่มี key สำหรับ runtime
- **ไม่ส่ง credential กลับ UI:** API ส่งเฉพาะชื่อผู้ให้บริการ, สถานะ, account reference ที่ปกปิด, mode และเวลาซิงค์ ไม่ส่ง plaintext หรือ ciphertext ของ credential กลับ client
- **PDPA consent:** ต้องกดยอมรับเองก่อนเชื่อมต่อ บันทึก `pdpaConsentedAt`, เวอร์ชันเอกสาร และวัตถุประสงค์สำหรับ audit; Demo Fill ไม่ติ๊กยินยอมให้อัตโนมัติ
- **Disconnect & Purge Data:** ลบ encrypted credentials และ consent receipt พร้อมลบ transaction/dividend ที่ติด provenance ของ Connector นั้นเท่านั้น ไม่ลบรายการที่ผู้ใช้ upload ด้วยตนเอง; คง audit metadata ขั้นต่ำแบบ append-only ตามนโยบาย retention ที่ต้องให้ฝ่ายกฎหมาย/DPO อนุมัติ
- **Decimal:** ใช้ `decimal.js` clone ที่ `precision: 40`, `ROUND_HALF_UP` สำหรับจำนวนเงิน, ค่าธรรมเนียม, fractional shares, FX และปันผล ก่อนแปลงเข้าสู่ CDM เดิม
- **Zero Core Rewrite:** ไม่แก้ `src/fifoEngine.ts`, `src/services/thaiTaxEngine.ts`, `src/services/fxRateService.ts`, `src/types.ts` หรือ `src/types/shared.ts`

## REST Contract

- `GET /api/thai-brokers/status` — สถานะ Bitkub / Dime! / Streaming และข้อความ roadmap
- `POST /api/thai-brokers/:broker/connect` — ต้องส่ง `pdpaConsent.accepted: true`; จัดเก็บ credential แบบ AES-GCM
- `POST /api/thai-brokers/:broker/sync` — ซิงค์ข้อมูล Read-Only และคืนจำนวน transaction/dividend ที่เพิ่มหรือข้ามซ้ำ
- `DELETE /api/thai-brokers/:broker/disconnect?purgeData=true` — ถอน consent, ลบ credential และ purge เฉพาะข้อมูลที่มาจาก connector

## หลักฐานและผลตรวจสอบ

- Backend: `tsc --noEmit` ผ่าน; **Jest 21/21 suites, 152/152 tests ผ่าน** รวม Bitkub mock → CDM/FIFO, AES-GCM, PDPA consent, idempotent sync และ purge transaction/dividend โดยคง manual CSV ไว้
- Frontend: `tsc --noEmit` และ Next.js production build ผ่าน; มี warning `react-hooks/exhaustive-deps` เดิมใน `Dashboard.tsx` (ไม่เกี่ยวกับ Thai Broker Hub)
- Playwright E2E ผ่าน ไม่มี HTTP 5xx: consent modal, เชื่อม Bitkub sandbox, Sync Now และ Disconnect & Purge Data
- Screenshots: `screenshots/46-thai-broker-hub-overview.png`, `screenshots/47-thai-broker-hub-pdpa-consent.png`, `screenshots/48-thai-broker-hub-sandbox-sync.png`, `screenshots/49-thai-broker-hub-purge-confirmed.png`

## Partner Discovery Checklist ก่อน Production

1. ขอเอกสาร API / statement format, API scope แบบ Read-Only, sandbox credentials และผู้รับผิดชอบการอนุมัติ
2. ยืนยัน rate-limit, IP allow-list, token rotation/expiry, incident escalation, error/retry policy และการ backfill ประวัติย้อนหลัง
3. อนุมัติ data-flow diagram, ผู้ควบคุม/ผู้ประมวลผลข้อมูล, retention, การส่งข้อมูลข้ามประเทศ, ช่องทางใช้สิทธิของเจ้าของข้อมูล และ privacy notice ฉบับเต็ม
4. ให้ Security, Legal/DPO และ Partner ทำ review / penetration test / sign-off ก่อนรับข้อมูลลูกค้าจริง
5. Bitkub API v3 ระบุ trade-history เป็น GET ที่ใช้ query `sym`, pagination และ HMAC; field `amount` มีความหมายต่างกันระหว่าง BUY (quote) และ SELL (base) จึงทำ mapping ตาม contract และไม่สร้าง VAT split จากข้อมูลที่ API ไม่ส่งมา

## ข้อจำกัดและการสื่อสารเชิงกำกับ

ป้าย **“Official Partner Integration Ready”** หมายถึงความพร้อมของผลิตภัณฑ์เพื่อเสนอให้คู่ค้าทบทวนทางเทคนิคเท่านั้น **ไม่ใช่การประกาศว่ามี partnership, endorsement, การอนุมัติจาก ก.ล.ต. หรือการรับรอง compliance** จาก Bitkub, Dime!, Settrade หรือตลาดหลักทรัพย์ฯ สถานะใบอนุญาต, permitted use, privacy notice และการตีความภาษีต้องตรวจสอบกับคู่ค้าและที่ปรึกษากฎหมายไทยก่อน Production

## เอกสารอ้างอิงสำหรับ Bitkub Adapter

- [Bitkub Official API v3 Documentation](https://github.com/bitkub/bitkub-official-api-docs) — HMAC headers, `GET /api/v3/market/my-order-history`, pagination และ field semantics
- [Bitkub Tax Guidelines for Cryptocurrency Trading](https://support.bitkub.com/en/support/solutions/articles/151000034551-tax-guidelines-for-cryptocurrency-trading) — แนวทาง VAT ของ Bitkub สำหรับธุรกรรมบนแพลตฟอร์ม
- [Bitkub FAQ for API Users](https://support.bitkub.com/en/support/solutions/articles/151000199019-faq-for-api-users) — Fee credits
