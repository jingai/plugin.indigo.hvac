FasdUAS 1.101.10   ��   ��    k             l     ��  ��    Q K Track Venstar thermostat changes (fan, furnace, and compressor on and off)     � 	 	 �   T r a c k   V e n s t a r   t h e r m o s t a t   c h a n g e s   ( f a n ,   f u r n a c e ,   a n d   c o m p r e s s o r   o n   a n d   o f f )   
  
 l     ��������  ��  ��        l     ��  ��    ' ! Creates the following variables:     �   B   C r e a t e s   t h e   f o l l o w i n g   v a r i a b l e s :      l     ��������  ��  ��        l     ��  ��    5 / AC_status (On, Off)		- compressor + fan status     �   ^   A C _ s t a t u s   ( O n ,   O f f ) 	 	 -   c o m p r e s s o r   +   f a n   s t a t u s      l     ��  ��    9 3 AC_Started (date)		- time of last call for cooling     �   f   A C _ S t a r t e d   ( d a t e ) 	 	 -   t i m e   o f   l a s t   c a l l   f o r   c o o l i n g      l     ��   ��    B < AC_dailymins (mins)		- total compressor runtime for the day      � ! ! x   A C _ d a i l y m i n s   ( m i n s ) 	 	 -   t o t a l   c o m p r e s s o r   r u n t i m e   f o r   t h e   d a y   " # " l     ��������  ��  ��   #  $ % $ l     �� & '��   & 5 / Heating_status (On, Off)	- heater + fan status    ' � ( ( ^   H e a t i n g _ s t a t u s   ( O n ,   O f f ) 	 -   h e a t e r   +   f a n   s t a t u s %  ) * ) l     �� + ,��   + = 7 Heating_Started (date)	- time of last call for heating    , � - - n   H e a t i n g _ S t a r t e d   ( d a t e ) 	 -   t i m e   o f   l a s t   c a l l   f o r   h e a t i n g *  . / . l     �� 0 1��   0 B < Heating_dailymins (mins)	- total heater runtime for the day    1 � 2 2 x   H e a t i n g _ d a i l y m i n s   ( m i n s ) 	 -   t o t a l   h e a t e r   r u n t i m e   f o r   t h e   d a y /  3 4 3 l     ��������  ��  ��   4  5 6 5 l     �� 7 8��   7 < 6 Fan_status (On, Off)		- On = Continuous fan operation    8 � 9 9 l   F a n _ s t a t u s   ( O n ,   O f f ) 	 	 -   O n   =   C o n t i n u o u s   f a n   o p e r a t i o n 6  : ; : l     �� < =��   < + %						- Off = Automatic fan operation    = � > > J 	 	 	 	 	 	 -   O f f   =   A u t o m a t i c   f a n   o p e r a t i o n ;  ? @ ? l     �� A B��   A L F Fan_Started (date)		- last manually initiated fan call (button press)    B � C C �   F a n _ S t a r t e d   ( d a t e ) 	 	 -   l a s t   m a n u a l l y   i n i t i a t e d   f a n   c a l l   ( b u t t o n   p r e s s ) @  D E D l     ��������  ��  ��   E  F G F l     �� H I��   H K E Filter_totalmins (mins)	- total fan runtime since last filter change    I � J J �   F i l t e r _ t o t a l m i n s   ( m i n s ) 	 -   t o t a l   f a n   r u n t i m e   s i n c e   l a s t   f i l t e r   c h a n g e G  K L K l     �� M N��   M . (						- this variable is manually reset!    N � O O P 	 	 	 	 	 	 -   t h i s   v a r i a b l e   i s   m a n u a l l y   r e s e t ! L  P Q P l     ��������  ��  ��   Q  R S R l      T U V T j     �� W�� ,0 thermostat_addresses Thermostat_Addresses W m      X X � Y Y 
 e m p t y U ) # automatically filled in at runtime    V � Z Z F   a u t o m a t i c a l l y   f i l l e d   i n   a t   r u n t i m e S  [ \ [ l     ��������  ��  ��   \  ] ^ ] i     _ ` _ I      �� a���� 20 _converthexstrtointeger _convertHexStrToInteger a  b�� b o      ���� 0 hexstr hexStr��  ��   ` k     � c c  d e d r      f g f m      h h � i i   0 1 2 3 4 5 6 7 8 9 A B C D E F g l      j���� j o      ���� 0 hexlist hexList��  ��   e  k l k s    F m n m o    ���� 0 hexstr hexStr n J       o o  p q p o      ���� 0 a1   q  r s r o      ���� 0 a2   s  t u t o      ���� 	0 skip1   u  v w v o      ���� 0 b1   w  x y x o      ���� 0 b2   y  z { z o      ���� 	0 skip2   {  | } | o      ���� 0 c1   }  ~�� ~ o      ���� 0 c2  ��   l   �  r   G T � � � \   G R � � � l  G P ����� � I  G P���� �
�� .sysooffslong    ��� null��   � �� � �
�� 
psof � o   I J���� 0 a1   � �� ���
�� 
psin � o   K L���� 0 hexlist hexList��  ��  ��   � m   P Q����  � o      ���� 0 a1o   �  � � � r   U b � � � \   U ` � � � l  U ^ ����� � I  U ^���� �
�� .sysooffslong    ��� null��   � �� � �
�� 
psof � o   W X���� 0 a1   � �� ���
�� 
psin � o   Y Z���� 0 hexlist hexList��  ��  ��   � m   ^ _����  � o      ���� 0 a1o   �  � � � r   c p � � � \   c n � � � l  c l ����� � I  c l���� �
�� .sysooffslong    ��� null��   � �� � �
�� 
psof � o   e f���� 0 a2   � �� ���
�� 
psin � o   g h���� 0 hexlist hexList��  ��  ��   � m   l m����  � o      ���� 0 a2o   �  � � � r   q ~ � � � \   q | � � � l  q z ����� � I  q z���� �
�� .sysooffslong    ��� null��   � �� � �
�� 
psof � o   s t���� 0 b1   � �� ���
�� 
psin � o   u v���� 0 hexlist hexList��  ��  ��   � m   z {����  � o      ���� 0 b1o   �  � � � r    � � � � \    � � � � l   � ����� � I   ����� �
�� .sysooffslong    ��� null��   � �� � �
�� 
psof � o   � ����� 0 b2   � �� ���
�� 
psin � o   � ����� 0 hexlist hexList��  ��  ��   � m   � �����  � o      ���� 0 b2o   �  � � � r   � � � � � \   � � � � � l  � � ����� � I  � ����� �
�� .sysooffslong    ��� null��   � �� � �
�� 
psof � o   � ����� 0 c1   � �� ���
�� 
psin � o   � ����� 0 hexlist hexList��  ��  ��   � m   � �����  � o      ���� 0 c1o   �  � � � r   � � � � � \   � � � � � l  � � ����� � I  � ����� �
�� .sysooffslong    ��� null��   � �� � �
�� 
psof � o   � ����� 0 c2   � �� ���
�� 
psin � o   � ����� 0 hexlist hexList��  ��  ��   � m   � ���  � o      �~�~ 0 c2o   �  � � � r   � � � � � ]   � � � � � ]   � � � � � m   � ��}�}  � m   � ��|�|  � l  � � ��{�z � [   � � � � � ]   � � � � � o   � ��y�y 0 a1o   � m   � ��x�x  � o   � ��w�w 0 a2o  �{  �z   � o      �v�v 0 val   �  � � � r   � � � � � [   � � � � � o   � ��u�u 0 val   � ]   � � � � � m   � ��t�t  � l  � � ��s�r � [   � � � � � ]   � � � � � o   � ��q�q 0 b1o   � m   � ��p�p  � o   � ��o�o 0 b2o  �s  �r   � o      �n�n 0 val   �  � � � r   � � � � � [   � � � � � [   � � � � � o   � ��m�m 0 val   � ]   � � � � � o   � ��l�l 0 c1o   � m   � ��k�k  � o   � ��j�j 0 c2o   � o      �i�i 0 val   �  ��h � L   � � � � o   � ��g�g 0 val  �h   ^  � � � l     �f�e�d�f  �e  �d   �  � � � w       � � � k       � �  � � � i    
 � � � I      �c ��b�c 0 read_indigo_variable   �  � � � o      �a�a 0 variable_name   �  �`  o      �_�_ 0 default_val  �`  �b   � k     )  l     �^�^   k e Read variable_name from Indigo's internal variable table.  Create the variable if it does not exist.    � �   R e a d   v a r i a b l e _ n a m e   f r o m   I n d i g o ' s   i n t e r n a l   v a r i a b l e   t a b l e .     C r e a t e   t h e   v a r i a b l e   i f   i t   d o e s   n o t   e x i s t .  Z     	
�]�\	 H     	 l    �[�Z I    �Y�X
�Y .coredoexbool        obj  4     �W
�W 
Vrbl l   �V�U o    �T�T 0 variable_name  �V  �U  �X  �[  �Z  
 I   �S�R
�S .corecrel****      � null�R   �Q
�Q 
kocl m    �P
�P 
Vrbl �O�N
�O 
prdt K     �M
�M 
pnam o    �L�L 0 variable_name   �K�J
�K 
Valu l   �I�H c     o    �G�G 0 default_val   m    �F
�F 
TEXT�I  �H  �J  �N  �]  �\   �E L   ! ) e   ! ( n   ! ( 1   % '�D
�D 
Valu l  ! % �C�B  4   ! %�A!
�A 
Vrbl! l  # $"�@�?" o   # $�>�> 0 variable_name  �@  �?  �C  �B  �E   � #$# l     �=�<�;�=  �<  �;  $ %&% i    '(' I      �:)�9�: 0 set_variable  ) *+* o      �8�8 0 variable_name  + ,�7, o      �6�6 0 variable_value  �7  �9  ( k     )-- ./. l     �501�5  0 5 / Set variable name into Indigo's variable table   1 �22 ^   S e t   v a r i a b l e   n a m e   i n t o   I n d i g o ' s   v a r i a b l e   t a b l e/ 3�43 Z     )45�364 H     	77 l    8�2�18 I    �09�/
�0 .coredoexbool        obj 9 4     �.:
�. 
Vrbl: l   ;�-�,; o    �+�+ 0 variable_name  �-  �,  �/  �2  �1  5 I   �*�)<
�* .corecrel****      � null�)  < �(=>
�( 
kocl= m    �'
�' 
Vrbl> �&?�%
�& 
prdt? K    @@ �$AB
�$ 
pnamA o    �#�# 0 variable_name  B �"C�!
�" 
ValuC l   D� �D c    EFE o    �� 0 variable_value  F m    �
� 
TEXT�   �  �!  �%  �3  6 r    )GHG l   "I��I c    "JKJ o     �� 0 variable_value  K m     !�
� 
TEXT�  �  H n      LML 1   & (�
� 
ValuM l  " &N��N 4   " &�O
� 
VrblO l  $ %P��P o   $ %�� 0 variable_name  �  �  �  �  �4  & QRQ l     ����  �  �  R STS i    UVU I      �W�� 0 log_thermostat  W XYX o      �� 0 log_text  Y Z�Z o      �
�
 0 action_name  �  �  V k     	[[ \]\ l     �	^_�	  ^ ? 9 Write Log_Text to the Indigo Log with the Thermostat Tag   _ �`` r   W r i t e   L o g _ T e x t   t o   t h e   I n d i g o   L o g   w i t h   t h e   T h e r m o s t a t   T a g] a�a I    	�bc
� .INDOLog null���    utf8b c     ded o     �� 0 log_text  e m    �
� 
TEXTc �f�
� 
LgTyf m    gg �hh  T h e r m o s t a t�  �  T iji l     ��� �  �  �   j klk i    mnm I      ��o���� 0 detect_on_or_off  o p��p o      ���� 0 	eventtype 	eventType��  ��  n L     qq =     rsr o     ���� 0 	eventtype 	eventTypes m    ��
�� EnITxF02l tut l     ��������  ��  ��  u vwv i    xyx I      ��z���� 0 update_filter_usage  z {��{ o      ���� 0 mins  ��  ��  y k     )|| }~} r     	� n    ��� I    ������� 0 read_indigo_variable  � ��� m    �� ���   F i l t e r _ t o t a l m i n s� ���� m    �� ���  0��  ��  �  f     � o      ���� 0 current_usage  ~ ��� r   
 ��� l  
 ������ [   
 ��� l  
 ������ c   
 ��� l  
 ������ o   
 ���� 0 current_usage  ��  ��  � m    ��
�� 
long��  ��  � l   ������ c    ��� l   ������ o    ���� 0 mins  ��  ��  � m    ��
�� 
long��  ��  ��  ��  � o      ���� 0 total_usage  � ��� n   ��� I    ������� 0 set_variable  � ��� m    �� ���   F i l t e r _ t o t a l m i n s� ���� o    ���� 0 total_usage  ��  ��  �  f    � ���� n   )��� I    )������� 0 log_thermostat  � ��� b    $��� b    "��� m    �� ���  F i l t e r   u s a g e :    � l   !������ c    !��� o    ���� 0 mins  � m     ��
�� 
TEXT��  ��  � m   " #�� ���    m i n u t e s� ���� m   $ %�� ���  ��  ��  �  f    ��  w ��� l     ��������  ��  ��  � ���� i    ��� I      ������� 0 detect_activity  � ��� o      ���� 0 groupnum groupNum� ���� o      ���� 0 	eventtype 	eventType��  ��  � k    ��� ��� r     ��� I     ������� 0 detect_on_or_off  � ���� o    ���� 0 	eventtype 	eventType��  ��  � o      ���� 0 activity  � ��� n  	 ��� I   
 ������� 0 set_variable  � ��� m   
 �� ��� 2 L a s t _ F u r n a c e _ S t a t e _ C h a n g e� ���� c    ��� l   ������ I   ������
�� .misccurdldt    ��� null��  ��  ��  ��  � m    ��
�� 
TEXT��  ��  �  f   	 
� ��� l   ��������  ��  ��  � ���� Z   ������ =   ��� o    ���� 0 groupnum groupNum� m    ���� � k    ��� ��� l   ������  �   Cooling   � ���    C o o l i n g� ��� Z    ������� =    ��� o    ���� 0 activity  � m    ��
�� boovtrue� k   # @�� ��� n  # *��� I   $ *������� 0 log_thermostat  � ��� m   $ %�� ��� $ R e q u e s t i n g   A C   -   O n� ���� m   % &�� ���  ��  ��  �  f   # $� ��� n  + 8��� I   , 8������� 0 set_variable  � ��� m   , -�� �    A C _ S t a r t e d� �� c   - 4 l  - 2���� I  - 2������
�� .misccurdldt    ��� null��  ��  ��  ��   m   2 3��
�� 
TEXT��  ��  �  f   + ,� �� n  9 @ I   : @������ 0 set_variable   	
	 m   : ; �  A C _ s t a t u s
 �� m   ; < �  O n��  ��    f   9 :��  ��  � k   C �  n  C J I   D J������ 0 log_thermostat    m   D E � & R e q u e s t i n g   A C   -   O f f �� m   E F �  ��  ��    f   C D  n  K R  I   L R��!���� 0 set_variable  ! "#" m   L M$$ �%%  A C _ s t a t u s# &��& m   M N'' �((  O f f��  ��     f   K L )*) n  S \+,+ I   T \��-���� 0 set_variable  - ./. m   T U00 �11  H e a t i n g _ s t a t u s/ 2��2 m   U X33 �44  O f f��  ��  ,  f   S T* 565 l  ] ]��������  ��  ��  6 787 r   ] n9:9 n  ] l;<; I   ^ l��=���� 0 read_indigo_variable  = >?> m   ^ a@@ �AA  A C _ S t a r t e d? B��B c   a hCDC l  a fE����E I  a f������
�� .misccurdldt    ��� null��  ��  ��  ��  D m   f g��
�� 
TEXT��  ��  <  f   ] ^: o      ���� 0 
start_date 
Start_Date8 FGF r   o }HIH \   o {JKJ l  o tL����L I  o t������
�� .misccurdldt    ��� null��  ��  ��  ��  K l  t zM����M 4   t z��N
�� 
ldt N l  x yO����O o   x y���� 0 
start_date 
Start_Date��  ��  ��  ��  I o      ���� 0 	time_diff  G PQP n  ~ �RSR I    ���T��� 0 log_thermostat  T UVU b    �WXW b    �YZY m    �[[ �\\  A C   R a n   f o r    Z l  � �]�~�}] c   � �^_^ _   � �`a` o   � ��|�| 0 	time_diff  a m   � ��{�{ <_ m   � ��z
�z 
TEXT�~  �}  X m   � �bb �cc    m i n u t e sV d�yd m   � �ee �ff  �y  �  S  f   ~ Q ghg r   � �iji n  � �klk I   � ��xm�w�x 0 read_indigo_variable  m non m   � �pp �qq  A C _ d a i l y m i n so r�vr m   � �ss �tt  0�v  �w  l  f   � �j o      �u�u 0 current_runtime  h uvu r   � �wxw l  � �y�t�sy c   � �z{z [   � �|}| l  � �~�r�q~ c   � �� l  � ���p�o� o   � ��n�n 0 current_runtime  �p  �o  � m   � ��m
�m 
long�r  �q  } l  � ���l�k� _   � ���� o   � ��j�j 0 	time_diff  � m   � ��i�i <�l  �k  { m   � ��h
�h 
long�t  �s  x o      �g�g 0 	dailymins  v ��� n  � ���� I   � ��f��e�f 0 set_variable  � ��� m   � ��� ���  A C _ d a i l y m i n s� ��d� o   � ��c�c 0 	dailymins  �d  �e  �  f   � �� ��� l  � ��b�a�`�b  �a  �`  � ��� l  � ��_���_  � F @ if fan is set to continuous (On), only update filter usage when   � ��� �   i f   f a n   i s   s e t   t o   c o n t i n u o u s   ( O n ) ,   o n l y   u p d a t e   f i l t e r   u s a g e   w h e n� ��� l  � ��^���^  � ' ! user sets it back to auto (Off).   � ��� B   u s e r   s e t s   i t   b a c k   t o   a u t o   ( O f f ) .� ��� r   � ���� n  � ���� I   � ��]��\�] 0 read_indigo_variable  � ��� m   � ��� ���  F a n _ s t a t u s� ��[� m   � ��� ���  O f f�[  �\  �  f   � �� o      �Z�Z 0 	fanstatus  � ��Y� Z   � ����X�W� =  � ���� o   � ��V�V 0 	fanstatus  � m   � ��� ���  O f f� n  � ���� I   � ��U��T�U 0 update_filter_usage  � ��S� _   � ���� o   � ��R�R 0 	time_diff  � m   � ��Q�Q <�S  �T  �  f   � ��X  �W  �Y  � ��P� l  � ��O�N�M�O  �N  �M  �P  � ��� =  � ���� o   � ��L�L 0 groupnum groupNum� m   � ��K�K � ��� k   ���� ��� l  � ��J���J  �   Heating   � ���    H e a t i n g� ��� Z   �����I�� =  � ���� o   � ��H�H 0 activity  � m   � ��G
�G boovtrue� k   ��� ��� n  � ��� I   � �F��E�F 0 log_thermostat  � ��� m   � ��� ��� . R e q u e s t i n g   H e a t i n g   -   O n� ��D� m   � ��� ���  �D  �E  �  f   � �� ��� n ��� I  �C��B�C 0 set_variable  � ��� m  �� ���  H e a t i n g _ S t a r t e d� ��A� c  ��� l 
��@�?� I 
�>�=�<
�> .misccurdldt    ��� null�=  �<  �@  �?  � m  
�;
�; 
TEXT�A  �B  �  f  � ��:� n ��� I  �9��8�9 0 set_variable  � ��� m  �� ���  H e a t i n g _ s t a t u s� ��7� m  �� ���  O n�7  �8  �  f  �:  �I  � k  ��� ��� n *��� I   *�6��5�6 0 log_thermostat  � ��� m   #�� ��� 0 R e q u e s t i n g   H e a t i n g   -   O f f� ��4� m  #&�� ���  �4  �5  �  f   � ��� n +6��� I  ,6�3 �2�3 0 set_variable     m  ,/ �  H e a t i n g _ s t a t u s �1 m  /2 �  O f f�1  �2  �  f  +,� 	 n 7B

 I  8B�0�/�0 0 set_variable    m  8; �  A C _ s t a t u s �. m  ;> �  O f f�.  �/    f  78	  l CC�-�,�+�-  �,  �+    r  CT n CR I  DR�*�)�* 0 read_indigo_variable    m  DG �    H e a t i n g _ S t a r t e d !�(! c  GN"#" l GL$�'�&$ I GL�%�$�#
�% .misccurdldt    ��� null�$  �#  �'  �&  # m  LM�"
�" 
TEXT�(  �)    f  CD o      �!�! 0 
start_date 
Start_Date %&% r  Uc'(' \  Ua)*) l UZ+� �+ I UZ���
� .misccurdldt    ��� null�  �  �   �  * l Z`,��, 4  Z`�-
� 
ldt - l ^_.��. o  ^_�� 0 
start_date 
Start_Date�  �  �  �  ( o      �� 0 	time_diff  & /0/ n d{121 I  e{�3�� 0 log_thermostat  3 454 b  et676 b  ep898 m  eh:: �;; , F u r n a c e   H e a t   R a n   f o r    9 l ho<��< c  ho=>= _  hm?@? o  hi�� 0 	time_diff  @ m  il�� <> m  mn�
� 
TEXT�  �  7 m  psAA �BB    m i n u t e s5 C�C m  twDD �EE  �  �  2  f  de0 FGF r  |�HIH n |�JKJ I  }��L�� 0 read_indigo_variable  L MNM m  }�OO �PP " H e a t i n g _ d a i l y m i n sN Q�
Q m  ��RR �SS  0�
  �  K  f  |}I o      �	�	 0 current_runtime  G TUT r  ��VWV l ��X��X c  ��YZY [  ��[\[ l ��]��] c  ��^_^ l ��`��` o  ���� 0 current_runtime  �  �  _ m  ���
� 
long�  �  \ l ��a� ��a _  ��bcb o  ������ 0 	time_diff  c m  ������ <�   ��  Z m  ����
�� 
long�  �  W o      ���� 0 	dailymins  U ded n ��fgf I  ����h���� 0 set_variable  h iji m  ��kk �ll " H e a t i n g _ d a i l y m i n sj m��m o  ������ 0 	dailymins  ��  ��  g  f  ��e non l ����������  ��  ��  o pqp l ����rs��  r F @ if fan is set to continuous (On), only update filter usage when   s �tt �   i f   f a n   i s   s e t   t o   c o n t i n u o u s   ( O n ) ,   o n l y   u p d a t e   f i l t e r   u s a g e   w h e nq uvu l ����wx��  w ' ! user sets it back to auto (Off).   x �yy B   u s e r   s e t s   i t   b a c k   t o   a u t o   ( O f f ) .v z{z r  ��|}| n ��~~ I  ��������� 0 read_indigo_variable  � ��� m  ���� ���  F a n _ s t a t u s� ���� m  ���� ���  O f f��  ��    f  ��} o      ���� 0 	fanstatus  { ���� Z  ��������� = ����� o  ������ 0 	fanstatus  � m  ���� ���  O f f� n ����� I  ��������� 0 update_filter_usage  � ���� _  ����� o  ������ 0 	time_diff  � m  ������ <��  ��  �  f  ����  ��  ��  � ���� l ����������  ��  ��  ��  � ��� = ����� o  ������ 0 groupnum groupNum� m  ������ � ���� k  ���� ��� l ��������  � > 8 Fan manually set to continuous (On) or automatic (Off).   � ��� p   F a n   m a n u a l l y   s e t   t o   c o n t i n u o u s   ( O n )   o r   a u t o m a t i c   ( O f f ) .� ���� Z  �������� = ����� o  ������ 0 activity  � m  ����
�� boovtrue� k  ��� ��� n ����� I  ��������� 0 log_thermostat  � ��� m  ���� ��� @ R e q u e s t i n g   F a n   -   O n   ( C o n t i n u o u s )� ���� m  ���� ���  ��  ��  �  f  ��� ��� n ����� I  ��������� 0 set_variable  � ��� m  ���� ���  F a n _ S t a r t e d� ���� c  ����� l �������� I ��������
�� .misccurdldt    ��� null��  ��  ��  ��  � m  ����
�� 
TEXT��  ��  �  f  ��� ���� n ���� I  �������� 0 set_variable  � ��� m  ���� ���  F a n _ s t a t u s� ���� m  ���� ���  O n��  ��  �  f  ����  ��  � k  ��� ��� n ��� I  ������� 0 log_thermostat  � ��� m  	�� ��� 6 R e q u e s t i n g   F a n   -   O f f   ( A u t o )� ���� m  	�� ���  ��  ��  �  f  � ��� n ��� I  ������� 0 set_variable  � ��� m  �� ���  F a n _ s t a t u s� ���� m  �� ���  O f f��  ��  �  f  � ��� l ��������  ��  ��  � ��� l ������  � C = only update filter usage if not currently cooling or heating   � ��� z   o n l y   u p d a t e   f i l t e r   u s a g e   i f   n o t   c u r r e n t l y   c o o l i n g   o r   h e a t i n g� ��� r  *��� n (��� I  (������� 0 read_indigo_variable  � ��� m  !�� ���  A C _ s t a t u s� ���� m  !$�� ���  O f f��  ��  �  f  � o      ���� 0 	ac_status 	AC_status� ��� r  +8��� n +6��� I  ,6�� ���� 0 read_indigo_variable     m  ,/ �  H e a t i n g _ s t a t u s �� m  /2 �  O f f��  ��  �  f  +,� o      ���� 0 heat_status Heat_status� �� Z  9�	
����	 l 9J���� F  9J = 9> o  9:���� 0 	ac_status 	AC_status m  := �  O f f = AF o  AB���� 0 heat_status Heat_status m  BE �  O f f��  ��  
 k  M�  l MM����   H B Fan_totalmins is also tallied in the dayend script, so if the fan    � �   F a n _ t o t a l m i n s   i s   a l s o   t a l l i e d   i n   t h e   d a y e n d   s c r i p t ,   s o   i f   t h e   f a n  l MM����   F @ has been running for longer than just today, only add up to the    �   �   h a s   b e e n   r u n n i n g   f o r   l o n g e r   t h a n   j u s t   t o d a y ,   o n l y   a d d   u p   t o   t h e !"! l MM��#$��  #   current day's usage.   $ �%% *   c u r r e n t   d a y ' s   u s a g e ." &'& r  M^()( n M\*+* I  N\��,���� 0 read_indigo_variable  , -.- m  NQ// �00  F a n _ S t a r t e d. 1��1 c  QX232 l QV4����4 I QV������
�� .misccurdldt    ��� null��  ��  ��  ��  3 m  VW��
�� 
TEXT��  ��  +  f  MN) o      ���� 0 
start_date 
Start_Date' 565 Z  _�78��97 l _s:����: = _s;<; l _i=����= n  _i>?> 1  ei��
�� 
dstr? 4  _e��@
�� 
ldt @ l cdA����A o  cd���� 0 
start_date 
Start_Date��  ��  ��  ��  < l irB����B n  irCDC 1  nr��
�� 
dstrD l inE����E I in������
�� .misccurdldt    ��� null��  ��  ��  ��  ��  ��  ��  ��  8 r  v�FGF \  v�HIH l v{J����J I v{������
�� .misccurdldt    ��� null��  ��  ��  ��  I l {�K����K 4  {���L
�� 
ldt L l �M����M o  ����� 0 
start_date 
Start_Date��  ��  ��  ��  G o      ���� 0 	time_diff  ��  9 r  ��NON \  ��PQP l ��R����R I ��������
�� .misccurdldt    ��� null��  ��  ��  ��  Q l ��S��~S 4  ���}T
�} 
ldt T l ��U�|�{U n  ��VWV 1  ���z
�z 
dstrW l ��X�y�xX I ���w�v�u
�w .misccurdldt    ��� null�v  �u  �y  �x  �|  �{  �  �~  O o      �t�t 0 	time_diff  6 YZY l ���s�r�q�s  �r  �q  Z [�p[ n ��\]\ I  ���o^�n�o 0 update_filter_usage  ^ _�m_ _  ��`a` o  ���l�l 0 	time_diff  a m  ���k�k <�m  �n  ]  f  ���p  ��  ��  ��  ��  ��  � n ��bcb I  ���jd�i�j 0 log_thermostat  d efe c  ��ghg b  ��iji m  ��kk �ll > I n v a l i d   g r o u p   n u m b e r   r e c e i v e d :  j l ��m�h�gm o  ���f�f 0 groupnum groupNum�h  �g  h m  ���e
�e 
TEXTf n�dn m  ��oo �pp  �d  �i  c  f  ����  ��   ��                                                                                  INDO  alis    t  kuramori                   �U�MH+   z{IndigoServer.app                                                �2f�d        ����  	                hvac    �Uǝ      ��P     z{ � �   ��  /kuramori:Users:jingai:dev:hvac:IndigoServer.app   "  I n d i g o S e r v e r . a p p    k u r a m o r i  &Users/jingai/dev/hvac/IndigoServer.app  /    ��   � qrq l     �c�b�a�c  �b  �a  r sts l     �`�_�^�`  �_  �^  t uvu l     �]wx�]  w b \--------------------------------------------------------------------------------------------   x �yy � - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v z�\z w      {|{ i    "}~} I     �[�
�[ .INDOpITNnull���   0 EnIT o      �Z�Z 0 	eventtype 	eventType� �Y��
�Y 
ToIA� o      �X�X 0 
addrstring 
addrString� �W��
�W 
GrpN� o      �V�V 0 groupnum groupNum� �U��
�U 
By  � o      �T�T 0 deltaval deltaVal� �S��R
�S 
StBn� o      �Q�Q 0 absval absVal�R  ~ k     ��� ��� Z     ^���P�O� =    ��� o     �N�N ,0 thermostat_addresses Thermostat_Addresses� m    �� ��� 
 e m p t y� l  
 Z���� k   
 Z�� ��� r   
 ��� J   
 �M�M  � o      �L�L ,0 thermostat_addresses Thermostat_Addresses� ��K� X    Z��J�� Z   % U���I�H� =  % *��� n   % (��� 1   & (�G
�G 
DvTp� o   % &�F�F 0 dev  � m   ( )�� ��� $ T h e r m o s t a t   A d a p t e r� k   - Q�� ��� r   - 7��� n  - 5��� I   . 5�E��D�E 20 _converthexstrtointeger _convertHexStrToInteger� ��C� n   . 1��� 1   / 1�B
�B 
X10a� o   . /�A�A 0 dev  �C  �D  �  f   - .� o      �@�@ 0 addrval addrVal� ��� r   8 E��� b   8 ?��� o   8 =�?�? ,0 thermostat_addresses Thermostat_Addresses� o   = >�>�> 0 addrval addrVal� o      �=�= ,0 thermostat_addresses Thermostat_Addresses� ��<� n  F Q��� I   G Q�;��:�; 0 log_thermostat  � ��� c   G L��� b   G J��� m   G H�� ��� 4 F o u n d   T h e r m o s t a t   A d a p t e r :  � l  H I��9�8� o   H I�7�7 0 addrval addrVal�9  �8  � m   J K�6
�6 
TEXT� ��5� m   L M�� ���  �5  �:  �  f   F G�<  �I  �H  �J 0 dev  � 2    �4
�4 
Devc�K  � 3 - only calculate first time we are ever called   � ��� Z   o n l y   c a l c u l a t e   f i r s t   t i m e   w e   a r e   e v e r   c a l l e d�P  �O  � ��� l  _ _�3�2�1�3  �2  �1  � ��� r   _ b��� m   _ `�0
�0 boovfals� o      �/�/ 0 
foundmatch 
foundMatch� ��� X   c ���.�� Z   w ����-�,� =   w ~��� l  w z��+�*� c   w z��� o   w x�)�) 0 devaddr devAddr� m   x y�(
�( 
long�+  �*  � l  z }��'�&� c   z }��� o   z {�%�% 0 
addrstring 
addrString� m   { |�$
�$ 
long�'  �&  � r   � ���� m   � ��#
�# boovtrue� o      �"�" 0 
foundmatch 
foundMatch�-  �,  �. 0 devaddr devAddr� o   f k�!�! ,0 thermostat_addresses Thermostat_Addresses� ��� Z   � ���� �� H   � ��� o   � ��� 0 
foundmatch 
foundMatch� k   � ��� ��� l  � �����  � J D my log_thermostat(addrString & " is not a Thermostat Adapter.", "")   � ��� �   m y   l o g _ t h e r m o s t a t ( a d d r S t r i n g   &   "   i s   n o t   a   T h e r m o s t a t   A d a p t e r . " ,   " " )� ��� l  � ����� L   � ���  � 0 * not a device address we are interested in   � ��� T   n o t   a   d e v i c e   a d d r e s s   w e   a r e   i n t e r e s t e d   i n�  �   �  � ��� l  � �����  �  �  � ��� n  � ���� I   � ����� 0 log_thermostat  � ��� m   � ��� ��� P I n s t e o n   T h e r m o s t a t   E v e n t   b e i n g   p r o c e s s e d� ��� m   � ��� ���  �  �  �  f   � �� ��� n  � ���� I   � ����� 0 detect_activity  � � � o   � ��� 0 groupnum groupNum  � o   � ��� 0 	eventtype 	eventType�  �  �  f   � �� � n  � � I   � ���� 0 log_thermostat    m   � � �		 X I n s t e o n   T h e r m o s t a t   E v e n t   p r o c e s s i n g   c o m p l e t e 
�
 m   � � �  �  �    f   � ��  |�                                                                                  INDO  alis    t  kuramori                   �U�MH+   z{IndigoServer.app                                                �2f�d        ����  	                hvac    �Uǝ      ��P     z{ � �   ��  /kuramori:Users:jingai:dev:hvac:IndigoServer.app   "  I n d i g o S e r v e r . a p p    k u r a m o r i  &Users/jingai/dev/hvac/IndigoServer.app  /    ��  �\       � X�   	�
�	��������
 ,0 thermostat_addresses Thermostat_Addresses�	 20 _converthexstrtointeger _convertHexStrToInteger� 0 read_indigo_variable  � 0 set_variable  � 0 log_thermostat  � 0 detect_on_or_off  � 0 update_filter_usage  � 0 detect_activity  
� .INDOpITNnull���   0 EnIT � `� ����� 20 _converthexstrtointeger _convertHexStrToInteger�  ����   ���� 0 hexstr hexStr��   ������������������������������������ 0 hexstr hexStr�� 0 hexlist hexList�� 0 a1  �� 0 a2  �� 	0 skip1  �� 0 b1  �� 0 b2  �� 	0 skip2  �� 0 c1  �� 0 c2  �� 0 a1o  �� 0 a2o  �� 0 b1o  �� 0 b2o  �� 0 c1o  �� 0 c2o  �� 0 val    h����������������������
�� 
cobj�� �� �� �� �� 
�� 
psof
�� 
psin
�� .sysooffslong    ��� null�� �� �� ��E�O�E[�k/EQ�Z[�l/EQ�Z[�m/EQ�Z[��/EQ�Z[��/EQ�Z[��/EQ�Z[��/EQ�Z[��/EQ�ZO*��� 	kE�O*��� 	kE�O*��� 	kE�O*��� 	kE�O*��� 	kE�O*��� 	kE�O*��� 	kE�O�� �� � E^ O] �� � E^ O] �� �E^ O]  �� ��������� 0 read_indigo_variable  �� ����   ������ 0 variable_name  �� 0 default_val  ��   ������ 0 variable_name  �� 0 default_val   	������������������
�� 
Vrbl
�� .coredoexbool        obj 
�� 
kocl
�� 
prdt
�� 
pnam
�� 
Valu
�� 
TEXT�� 
�� .corecrel****      � null�� **�/j  *������&�� Y hO*�/�,E ��(�������� 0 set_variable  �� ����   ������ 0 variable_name  �� 0 variable_value  ��   ������ 0 variable_name  �� 0 variable_value   	������������������
�� 
Vrbl
�� .coredoexbool        obj 
�� 
kocl
�� 
prdt
�� 
pnam
�� 
Valu
�� 
TEXT�� 
�� .corecrel****      � null�� **�/j  *������&�� Y ��&*�/�,F ��V���� ���� 0 log_thermostat  �� ��!�� !  ������ 0 log_text  �� 0 action_name  ��   ������ 0 log_text  �� 0 action_name    ����g��
�� 
TEXT
�� 
LgTy
�� .INDOLog null���    utf8�� 
��&��l  ��n����"#���� 0 detect_on_or_off  �� ��$�� $  ���� 0 	eventtype 	eventType��  " ���� 0 	eventtype 	eventType# ��
�� EnITxF02�� ��  ��y����%&���� 0 update_filter_usage  �� ��'�� '  ���� 0 mins  ��  % �������� 0 mins  �� 0 current_usage  �� 0 total_usage  & ������������������ 0 read_indigo_variable  
�� 
long�� 0 set_variable  
�� 
TEXT�� 0 log_thermostat  �� *)��l+ E�O��&��&E�O)�l+ O)��&%�%�l+ 
 �������()���� 0 detect_activity  �� ��*�� *  ������ 0 groupnum groupNum�� 0 	eventtype 	eventType��  ( 
���������������������� 0 groupnum groupNum�� 0 	eventtype 	eventType�� 0 activity  �� 0 
start_date 
Start_Date�� 0 	time_diff  �� 0 current_runtime  �� 0 	dailymins  �� 0 	fanstatus  �� 0 	ac_status 	AC_status�� 0 heat_status Heat_status) I��������������$'03@����[��beps��������������:ADORk���������������~/�}ko�� 0 detect_on_or_off  
�� .misccurdldt    ��� null
�� 
TEXT�� 0 set_variable  �� 0 log_thermostat  �� 0 read_indigo_variable  
�� 
ldt �� <
�� 
long� 0 update_filter_usage  
�~ 
bool
�} 
dstr���*�k+  E�O)�*j �&l+ O�k  ΢e  ")��l+ O)�*j �&l+ O)��l+ Y �)��l+ O)��l+ O)�a l+ O)a *j �&l+ E�O*j *a �/E�O)a �a "�&%a %a l+ O)a a l+ E�O�a &�a "a &E�O)a �l+ O)a a l+ E�O�a   )�a "k+ Y hOPYؠl  �e  ,)a  a !l+ O)a "*j �&l+ O)a #a $l+ Y �)a %a &l+ O)a 'a (l+ O)a )a *l+ O)a +*j �&l+ E�O*j *a �/E�O)a ,�a "�&%a -%a .l+ O)a /a 0l+ E�O�a &�a "a &E�O)a 1�l+ O)a 2a 3l+ E�O�a 4  )�a "k+ Y hOPY �m  ݢe  ,)a 5a 6l+ O)a 7*j �&l+ O)a 8a 9l+ Y �)a :a ;l+ O)a <a =l+ O)a >a ?l+ E�O)a @a Al+ E�O�a B 	 �a C a D& a)a E*j �&l+ E�O*a �/a F,*j a F,  *j *a �/E�Y *j *a *j a F,E/E�O)�a "k+ Y hY )a G�%�&a Hl+  �|~�{�z+,�y
�| .INDOpITNnull���   0 EnIT�{ 0 	eventtype 	eventType�z �x�w-
�x 
ToIA�w 0 
addrstring 
addrString- �v�u.
�v 
GrpN�u 0 groupnum groupNum. �t�s/
�t 
By  �s 0 deltaval deltaVal/ �r�q�p
�r 
StBn�q 0 absval absVal�p  + 	�o�n�m�l�k�j�i�h�g�o 0 	eventtype 	eventType�n 0 
addrstring 
addrString�m 0 groupnum groupNum�l 0 deltaval deltaVal�k 0 absval absVal�j 0 dev  �i 0 addrval addrVal�h 0 
foundmatch 
foundMatch�g 0 devaddr devAddr, ��f�e�d�c�b��a�`��_��^�]���\
�f 
Devc
�e 
kocl
�d 
cobj
�c .corecnte****       ****
�b 
DvTp
�a 
X10a�` 20 _converthexstrtointeger _convertHexStrToInteger
�_ 
TEXT�^ 0 log_thermostat  
�] 
long�\ 0 detect_activity  �y �b   �  UjvEc   O F*�-[��l kh ��,�  ))��,k+ E�Ob   �%Ec   O)�%�&�l+ Y h[OY��Y hOfE�O )b   [��l kh ��&��&  eE�Y h[OY��O� hY hO)��l+ O)��l+ O)a a l+  ascr  ��ޭ