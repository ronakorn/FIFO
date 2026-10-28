import json
from pathlib import Path
root=Path('/home/user/fifo-wealth-os-web/messages')
extra={
'en':{
 'profile':{'boundaryTitle':'Unable to load the profile page','verifiedSession':'Verified JWT session','logout':'Sign out','guestMode':'Guest mode (preview)','guestDescription':'Sign in to save portfolios and generate personal tax report PDFs.','loginRegister':'Sign in / Create account','rmfDateTitle':'Date of birth for the RMF age condition (optional)','rmfDateDescription':'Used only to show age-55 status in the fund dashboard. This does not confirm tax eligibility or redemption requirements. Leave it blank and save to remove it.','dateOfBirth':'Date of birth','dateOfBirthAria':'Date of birth for the RMF age condition','saveDateOfBirth':'Save date of birth','dateSaved':'Date of birth saved. It is used only to display the RMF age status.','loadBirthError':'Unable to load date of birth: {error}','loadBirthErrorFallback':'Unable to load date-of-birth details.','appearanceHeading':'Appearance','appearanceIntro':'Choose a minimal light theme or a WCAG AA-friendly dark theme.','lightTheme':'Light minimalist','darkTheme':'Dark charcoal','defaultTaxYear':'Default tax year','taxYearDescription':'Used for shortcuts to P.N.D. 90/91 reports.'},
 'billing':{'zeroMonthly':'THB 0 / month'},
 'support':{'betaPlanAccess':'Open Beta Plan · All Access'}
},
'th':{
 'profile':{'boundaryTitle':'ไม่สามารถโหลดหน้าโปรไฟล์ได้','verifiedSession':'ยืนยันเซสชัน JWT แล้ว','logout':'ออกจากระบบ','guestMode':'โหมดผู้เยี่ยมชม (Preview Mode)','guestDescription':'เข้าสู่ระบบเพื่อบันทึกพอร์ตและออกรายงานภาษี PDF ส่วนบุคคล','loginRegister':'เข้าสู่ระบบ / สมัครสมาชิก','rmfDateTitle':'วันเกิดสำหรับตรวจเงื่อนไขอายุ RMF (ไม่บังคับ)','rmfDateDescription':'ใช้แสดงสถานะอายุ 55 ปีในแดชบอร์ดกองทุนเท่านั้น ไม่ใช่การยืนยันสิทธิ์ทางภาษีหรือข้อกำหนดการขายคืน หากต้องการลบข้อมูล ให้เว้นว่างแล้วบันทึก','dateOfBirth':'วัน / เดือน / ปีเกิด','dateOfBirthAria':'วันเกิดสำหรับเงื่อนไขอายุ RMF','saveDateOfBirth':'บันทึกวันเกิด','dateSaved':'บันทึกวันเกิดแล้ว ใช้สำหรับแสดงสถานะอายุ RMF เท่านั้น','loadBirthError':'ไม่สามารถโหลดข้อมูลวันเกิดได้: {error}','loadBirthErrorFallback':'ไม่สามารถโหลดรายละเอียดวันเกิดได้','appearanceHeading':'โหมดการแสดงผล','appearanceIntro':'เลือกโหมดสว่างมินิมอล หรือโหมดมืดถนอมสายตาที่ผ่านมาตรฐาน WCAG AA','lightTheme':'โหมดสว่างมินิมอล','darkTheme':'โหมดมืด Charcoal','defaultTaxYear':'ปีภาษีเริ่มต้น','taxYearDescription':'ใช้สำหรับทางลัดเปิดรายงาน ภ.ง.ด. 90/91'},
 'billing':{'zeroMonthly':'0 บาท / เดือน'},
 'support':{'betaPlanAccess':'แผน Open Beta · ใช้งานได้ทุกฟีเจอร์'}
}
}
for lang,tree in extra.items():
 p=root/f'{lang}.json'; d=json.loads(p.read_text())
 for ns,vals in tree.items(): d[ns].update(vals)
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 print(lang,'updated')
