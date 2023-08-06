(LazyEmployee) Employee OOP for Testing PyPI by Tun Kedsaro

==============================================

โปรแกรมแชทนี้เป็นโปรแกรมที่เขียนขึ้นมาโดยใช้ Python โดยการเขียนแบบ OOP
สำหรับใช้งานในการสร้าง class employee อย่างรวดเร็ว เพียงแค่มี Python
อยู่ในคอมพิวเตอร์ก็สามารถใช้งานได้เลย เบื้องหลังการทำงานจะประกอบไปด้วย
Engineer,Accounting,Sale

ปล. เวอร์ชั่นนี้ยังไม่สมบูรณ์ (เขียนแบบรีบๆ) เขียนเพื่อนำ concept OOP
มาสร้าง library แล้วก็ upload ขึ้น Github กับ PyPI ต่อไป
สำหรับนักพัฒนาสามารถนำ Source Code ไปพัฒนาต่อได้เต็มที่
ซึ่งก็คืออีกโปรเจคนึ่งนั้นแหละ เพราะว่า jupyter มันไม่สามารถ import def
ได้เหมือนกับตัว คอมก็เลยใช้วิธีนี้เอา และก็ยังมีอีกหลาย library
ที่เขียนดองเอาไว้ตั้งแต่สมัยเรียน ปี3, 4 แต่ว่ายังไม่ได้ upload
(เขียนไปงั้นแหละต้องใช้ความยาวระดับหนึ่งไม่งั้นไม่สามารถอัพได้)

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

    pip install lazyemployee

วิธีใช้
~~~~~~~

[STEP 1] - เปิด IDLE ขึ้นมาแล้วพิมพ์...

.. code:: python

   from lazyemployee import Employee
   from lazyemployee import Accounting,Programmer,Sale

-  หรือเปิด cmd / terminal แล้วพิมพ์

.. code:: python

   python -m lazyemployee

[STEP 2] - ประกาศ class employee กรอก ชื่อ ตำแหน่งงาน และ เงินเดือน -
สามารถเรียกการแสดงผลได้โดยการใช้คำสั่ง detail() -
สามารถเปลี่ยนข้อมูลข้างในได้ด้วยการใช้ฟังก์ชัน setname()
,setsalary(),setjob() - สามารถรับค่าข้อมูลข้างในได้ด้วยการใช้ฟังก์ชัน
getname() ,getsalary(),getjob()



[STEP 3] - ใช้งานได้เลยจ้าาา

Develop by : Tun Kedsaro 
FB: I dont tell you. 
YouTube: Tun Kedsaro

