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
Vrbl 6 l  ' ( 7���� 7 o   ' (���� 0 variable_name  ��  ��  ��  ��  ��    m      8 8                                                                                  INDO  alis    �  MacOS                      �ىH+   �ܹIndigoServer.app                                                �ܻř/m        ����  	                Indigo 4    ��      řu�     �ܹy����X  QMacOS:Library:Application Support:Perceptive Automation:Indigo 4:IndigoServer.app   "  I n d i g o S e r v e r . a p p    M a c O S  KLibrary/Application Support/Perceptive Automation/Indigo 4/IndigoServer.app   / ��     9 : 9 l     ��������  ��  ��   :  ; < ; i     = > = I      �� ?���� 0 set_variable   ?  @ A @ o      ���� 0 variable_name   A  B�� B o      ���� 0 variable_value  ��  ��   > O     . C D C k    - E E  F G F l   �� H I��   H 5 / Set variable name into Indigo's variable table    I � J J ^   S e t   v a r i a b l e   n a m e   i n t o   I n d i g o ' s   v a r i a b l e   t a b l e G  K�� K Z    - L M�� N L H     O O l    P���� P I   �� Q��
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
Vrbl g l  ( ) h���� h o   ( )���� 0 variable_name  ��  ��  ��  ��  ��   D m      i i                                                                                  INDO  alis    �  MacOS                      �ىH+   �ܹIndigoServer.app                                                �ܻř/m        ����  	                Indigo 4    ��      řu�     �ܹy����X  QMacOS:Library:Application Support:Perceptive Automation:Indigo 4:IndigoServer.app   "  I n d i g o S e r v e r . a p p    M a c O S  KLibrary/Application Support/Perceptive Automation/Indigo 4/IndigoServer.app   / ��   <  j k j l     ��������  ��  ��   k  l m l i     n o n I      �� p���� 0 log_thermostat   p  q r q o      ���� 0 log_text   r  s�� s o      ���� 0 action_name  ��  ��   o O      t u t I   �� v w
�� .INDOLog null���    utf8 v c     x y x o    ���� 0 log_text   y m    ��
�� 
TEXT w �� z��
�� 
LgTy z m    	 { { � | |  T h e r m o s t a t��   u m      } }                                                                                  INDO  alis    �  MacOS                      �ىH+   �ܹIndigoServer.app                                                �ܻř/m        ����  	                Indigo 4    ��      řu�     �ܹy����X  QMacOS:Library:Application Support:Perceptive Automation:Indigo 4:IndigoServer.app   "  I n d i g o S e r v e r . a p p    M a c O S  KLibrary/Application Support/Perceptive Automation/Indigo 4/IndigoServer.app   / ��   m  ~  ~ l     ��������  ��  ��     � � � l     �� � ���   � 9 3 these MUST be set first for plotting to work right    � � � � f   t h e s e   M U S T   b e   s e t   f i r s t   f o r   p l o t t i n g   t o   w o r k   r i g h t �  � � � l     ����� � n     � � � I    �� ����� 0 set_variable   �  � � � m     � � � � �  A C _ d a i l y m i n s �  ��� � m    ����  ��  ��   �  f     ��  ��   �  � � � l    ����� � n    � � � I   	 �� ����� 0 set_variable   �  � � � m   	 
 � � � � � " H e a t i n g _ d a i l y m i n s �  ��� � m   
 ����  ��  ��   �  f    	��  ��   �  � � � l     ��������  ��  ��   �  � � � l     �� � ���   � n h if heating or cooling has rolled over from the previous day, re-set the *_Started variables for the new    � � � � �   i f   h e a t i n g   o r   c o o l i n g   h a s   r o l l e d   o v e r   f r o m   t h e   p r e v i o u s   d a y ,   r e - s e t   t h e   * _ S t a r t e d   v a r i a b l e s   f o r   t h e   n e w �  � � � l     �� � ���   � ' ! day to indicate On state on plot    � � � � B   d a y   t o   i n d i c a t e   O n   s t a t e   o n   p l o t �  � � � l    ����� � r     � � � n    � � � I    �� ����� 0 read_indigo_variable   �  � � � m     � � � � �  A C _ s t a t u s �  ��� � m     � � � � �  O f f��  ��   �  f     � o      ���� 0 	ac_status 	AC_status��  ��   �  � � � l   1 ���� � Z    1 � ��~�} � =    � � � o    �|�| 0 	ac_status 	AC_status � m     � � � � �  O n � n    - � � � I   ! -�{ ��z�{ 0 set_variable   �  � � � m   ! " � � � � �  A C _ S t a r t e d �  ��y � c   " ) � � � l  " ' ��x�w � I  " '�v�u�t
�v .misccurdldt    ��� null�u  �t  �x  �w   � m   ' (�s
�s 
TEXT�y  �z   �  f     !�~  �}  ��  �   �  � � � l  2 ; ��r�q � r   2 ; � � � n  2 9 � � � I   3 9�p ��o�p 0 read_indigo_variable   �  � � � m   3 4 � � � � �  H e a t i n g _ s t a t u s �  ��n � m   4 5 � � � � �  O f f�n  �o   �  f   2 3 � o      �m�m 0 heat_status Heat_status�r  �q   �  ��l � l  < S ��k�j � Z   < S � ��i�h � =  < ? � � � o   < =�g�g 0 heat_status Heat_status � m   = > � � � � �  O n � n  B O � � � I   C O�f ��e�f 0 set_variable   �  � � � m   C D � � � � �  H e a t i n g _ S t a r t e d �  ��d � c   D K � � � l  D I ��c�b � I  D I�a�`�_
�a .misccurdldt    ��� null�`  �_  �c  �b   � m   I J�^
�^ 
TEXT�d  �e   �  f   B C�i  �h  �k  �j  �l       
�] � � � � � � ��\�[�]   � �Z�Y�X�W�V�U�T�S�Z 0 read_indigo_variable  �Y 0 set_variable  �X 0 log_thermostat  
�W .aevtoappnull  �   � ****�V 0 	ac_status 	AC_status�U 0 heat_status Heat_status�T  �S   � �R �Q�P � ��O�R 0 read_indigo_variable  �Q �N ��N  �  �M�L�M 0 variable_name  �L 0 default_val  �P   � �K�J�K 0 variable_name  �J 0 default_val   � 
 8�I�H�G�F�E�D�C�B�A
�I 
Vrbl
�H .coredoexbool        obj 
�G 
kocl
�F 
prdt
�E 
pnam
�D 
Valu
�C 
TEXT�B 
�A .corecrel****      � null�O /� +*�/j  *������&�� 	Y hO*�/�,EU � �@ >�?�> � ��=�@ 0 set_variable  �? �< ��<  �  �;�:�; 0 variable_name  �: 0 variable_value  �>   � �9�8�9 0 variable_name  �8 0 variable_value   � 
 i�7�6�5�4�3�2�1�0�/
�7 
Vrbl
�6 .coredoexbool        obj 
�5 
kocl
�4 
prdt
�3 
pnam
�2 
Valu
�1 
TEXT�0 
�/ .corecrel****      � null�= /� +*�/j  *������&�� 	Y ��&*�/�,FU � �. o�-�, � ��+�. 0 log_thermostat  �- �* ��*  �  �)�(�) 0 log_text  �( 0 action_name  �,   � �'�&�' 0 log_text  �& 0 action_name   �  }�%�$ {�#
�% 
TEXT
�$ 
LgTy
�# .INDOLog null���    utf8�+ � ��&��l U � �" ��!�  � ��
�" .aevtoappnull  �   � **** � k     S � �  �    �  �  �  �  ���  �!  �    �   �  �� � � ��� � ��� � �� � �� 0 set_variable  � 0 read_indigo_variable  � 0 	ac_status 	AC_status
� .misccurdldt    ��� null
� 
TEXT� 0 heat_status Heat_status� T)�jl+ O)�jl+ O)��l+ E�O��  )�*j 	�&l+ Y hO)��l+ E�O��  )�*j 	�&l+ Y h � �  O f f � �  O f f�\  �[   ascr  ��ޭ