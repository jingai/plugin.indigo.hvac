FasdUAS 1.101.10   ��   ��    k             l     ��  ��    E ?  Reset thermostat usage variables, activated once/day at 0:00.     � 	 	 ~     R e s e t   t h e r m o s t a t   u s a g e   v a r i a b l e s ,   a c t i v a t e d   o n c e / d a y   a t   0 : 0 0 .   
  
 l     ��������  ��  ��        i         I      �� ���� 0 read_indigo_variable        o      ���� 0 variable_name     ��  o      ���� 0 default_val  ��  ��    O     .    k    -       l   ��  ��    k e Read variable_name from Indigo's internal variable table.  Create the variable if it does not exist.     �   �   R e a d   v a r i a b l e _ n a m e   f r o m   I n d i g o ' s   i n t e r n a l   v a r i a b l e   t a b l e .     C r e a t e   t h e   v a r i a b l e   i f   i t   d o e s   n o t   e x i s t .      Z   $  ����  H         l    !���� ! I   �� "��
�� .coredoexbool        obj  " 4    �� #
�� 
Vrbl # l    $���� $ o    ���� 0 variable_name  ��  ��  ��  ��  ��    I    ���� %
�� .corecrel****      � null��   % �� & '
�� 
kocl & m    ��
�� 
Vrbl ' �� (��
�� 
prdt ( K     ) ) �� * +
�� 
pnam * o    ���� 0 variable_name   + �� ,��
�� 
Valu , l    -���� - c     . / . o    ���� 0 default_val   / m    ��
�� 
TEXT��  ��  ��  ��  ��  ��     0�� 0 L   % - 1 1 e   % , 2 2 n   % , 3 4 3 1   ) +��
�� 
Valu 4 l  % ) 5���� 5 4   % )�� 6
�� 
Vrbl 6 l  ' ( 7���� 7 o   ' (���� 0 variable_name  ��  ��  ��  ��  ��    m      8 8�                                                                                  INDO  alis    t  kuramori                   �U�MH+   z{IndigoServer.app                                                �2f�d        ����  	                hvac    �Uǝ      ��P     z{ � �   ��  /kuramori:Users:jingai:dev:hvac:IndigoServer.app   "  I n d i g o S e r v e r . a p p    k u r a m o r i  &Users/jingai/dev/hvac/IndigoServer.app  /    ��     9 : 9 l     ��������  ��  ��   :  ; < ; i     = > = I      �� ?���� 0 set_variable   ?  @ A @ o      ���� 0 variable_name   A  B�� B o      ���� 0 variable_value  ��  ��   > O     . C D C k    - E E  F G F l   �� H I��   H 5 / Set variable name into Indigo's variable table    I � J J ^   S e t   v a r i a b l e   n a m e   i n t o   I n d i g o ' s   v a r i a b l e   t a b l e G  K�� K Z    - L M�� N L H     O O l    P���� P I   �� Q��
�� .coredoexbool        obj  Q 4    �� R
�� 
Vrbl R l    S���� S o    ���� 0 variable_name  ��  ��  ��  ��  ��   M I    ���� T
�� .corecrel****      � null��   T �� U V
�� 
kocl U m    ��
�� 
Vrbl V �� W��
�� 
prdt W K     X X �� Y Z
�� 
pnam Y o    ���� 0 variable_name   Z �� [��
�� 
Valu [ l    \���� \ c     ] ^ ] o    ���� 0 variable_value   ^ m    ��
�� 
TEXT��  ��  ��  ��  ��   N r   # - _ ` _ l  # & a���� a c   # & b c b o   # $���� 0 variable_value   c m   $ %��
�� 
TEXT��  ��   ` n       d e d 1   * ,��
�� 
Valu e l  & * f���� f 4   & *�� g
�� 
Vrbl g l  ( ) h���� h o   ( )���� 0 variable_name  ��  ��  ��  ��  ��   D m      i i�                                                                                  INDO  alis    t  kuramori                   �U�MH+   z{IndigoServer.app                                                �2f�d        ����  	                hvac    �Uǝ      ��P     z{ � �   ��  /kuramori:Users:jingai:dev:hvac:IndigoServer.app   "  I n d i g o S e r v e r . a p p    k u r a m o r i  &Users/jingai/dev/hvac/IndigoServer.app  /    ��   <  j k j l     ��������  ��  ��   k  l m l i     n o n I      �� p���� 0 log_thermostat   p  q r q o      ���� 0 log_text   r  s�� s o      ���� 0 action_name  ��  ��   o O      t u t I   �� v w
�� .INDOLog null���    utf8 v c     x y x o    ���� 0 log_text   y m    ��
�� 
TEXT w �� z��
�� 
LgTy z m    	 { { � | |  T h e r m o s t a t��   u m      } }�                                                                                  INDO  alis    t  kuramori                   �U�MH+   z{IndigoServer.app                                                �2f�d        ����  	                hvac    �Uǝ      ��P     z{ � �   ��  /kuramori:Users:jingai:dev:hvac:IndigoServer.app   "  I n d i g o S e r v e r . a p p    k u r a m o r i  &Users/jingai/dev/hvac/IndigoServer.app  /    ��   m  ~  ~ l     ��������  ��  ��     � � � l     ����� � n     � � � I    �� ����� 0 set_variable   �  � � � m     � � � � �  A C _ d a i l y m i n s �  ��� � m    ����  ��  ��   �  f     ��  ��   �  � � � l    ����� � n    � � � I   	 �� ����� 0 set_variable   �  � � � m   	 
 � � � � � " H e a t i n g _ d a i l y m i n s �  ��� � m   
 ����  ��  ��   �  f    	��  ��   �  � � � l     ��������  ��  ��   �  � � � l     �� � ���   � n h if heating or cooling has rolled over from the previous day, re-set the *_Started variables for the new    � � � � �   i f   h e a t i n g   o r   c o o l i n g   h a s   r o l l e d   o v e r   f r o m   t h e   p r e v i o u s   d a y ,   r e - s e t   t h e   * _ S t a r t e d   v a r i a b l e s   f o r   t h e   n e w �  � � � l     �� � ���   � ' ! day to indicate On state on plot    � � � � B   d a y   t o   i n d i c a t e   O n   s t a t e   o n   p l o t �  � � � l    ����� � r     � � � n    � � � I    �� ����� 0 read_indigo_variable   �  � � � m     � � � � �  A C _ s t a t u s �  ��� � m     � � � � �  O f f��  ��   �  f     � o      ���� 0 	ac_status 	AC_status��  ��   �  � � � l   1 ����� � Z    1 � ���~ � =    � � � o    �}�} 0 	ac_status 	AC_status � m     � � � � �  O n � n    - � � � I   ! -�| ��{�| 0 set_variable   �  � � � m   ! " � � � � �  A C _ S t a r t e d �  ��z � c   " ) � � � l  " ' ��y�x � I  " '�w�v�u
�w .misccurdldt    ��� null�v  �u  �y  �x   � m   ' (�t
�t 
TEXT�z  �{   �  f     !�  �~  ��  ��   �  � � � l  2 ; ��s�r � r   2 ; � � � n  2 9 � � � I   3 9�q ��p�q 0 read_indigo_variable   �  � � � m   3 4 � � � � �  H e a t i n g _ s t a t u s �  ��o � m   4 5 � � � � �  O f f�o  �p   �  f   2 3 � o      �n�n 0 heat_status Heat_status�s  �r   �  ��m � l  < S ��l�k � Z   < S � ��j�i � =  < ? � � � o   < =�h�h 0 heat_status Heat_status � m   = > � � � � �  O n � n  B O � � � I   C O�g ��f�g 0 set_variable   �  � � � m   C D � � � � �  H e a t i n g _ S t a r t e d �  ��e � c   D K � � � l  D I ��d�c � I  D I�b�a�`
�b .misccurdldt    ��� null�a  �`  �d  �c   � m   I J�_
�_ 
TEXT�e  �f   �  f   B C�j  �i  �l  �k  �m       �^ � � � � ��^   � �]�\�[�Z�] 0 read_indigo_variable  �\ 0 set_variable  �[ 0 log_thermostat  
�Z .aevtoappnull  �   � **** � �Y �X�W � ��V�Y 0 read_indigo_variable  �X �U ��U  �  �T�S�T 0 variable_name  �S 0 default_val  �W   � �R�Q�R 0 variable_name  �Q 0 default_val   � 
 8�P�O�N�M�L�K�J�I�H
�P 
Vrbl
�O .coredoexbool        obj 
�N 
kocl
�M 
prdt
�L 
pnam
�K 
Valu
�J 
TEXT�I 
�H .corecrel****      � null�V /� +*�/j  *������&�� 	Y hO*�/�,EU � �G >�F�E � ��D�G 0 set_variable  �F �C ��C  �  �B�A�B 0 variable_name  �A 0 variable_value  �E   � �@�?�@ 0 variable_name  �? 0 variable_value   � 
 i�>�=�<�;�:�9�8�7�6
�> 
Vrbl
�= .coredoexbool        obj 
�< 
kocl
�; 
prdt
�: 
pnam
�9 
Valu
�8 
TEXT�7 
�6 .corecrel****      � null�D /� +*�/j  *������&�� 	Y ��&*�/�,FU � �5 o�4�3 � ��2�5 0 log_thermostat  �4 �1 ��1  �  �0�/�0 0 log_text  �/ 0 action_name  �3   � �.�-�. 0 log_text  �- 0 action_name   �  }�,�+ {�*
�, 
TEXT
�+ 
LgTy
�* .INDOLog null���    utf8�2 � ��&��l U � �) ��(�' � ��&
�) .aevtoappnull  �   � **** � k     S � �  � � �  � � �  � � �  � � �  � � �  ��%�%  �(  �'   �   �  ��$ � � ��#�" � ��!�  � �� � ��$ 0 set_variable  �# 0 read_indigo_variable  �" 0 	ac_status 	AC_status
�! .misccurdldt    ��� null
�  
TEXT� 0 heat_status Heat_status�& T)�jl+ O)�jl+ O)��l+ E�O��  )�*j 	�&l+ Y hO)��l+ E�O��  )�*j 	�&l+ Y hascr  ��ޭ