### �g�p�@
python3 add-caption-and-margin.py csv_path.csv [start_index]

- csv_path.csv ��ǂݎ���Ĉ�s���Ƃɉ摜����������
  - start_index ���w�肷��� csv_path.csv �� start_index �s�ڂ��珈�����J�n����

### csv �̏���

|filepath|outputname|width|height|anchor_x|anchor_y|margin|comment|
|:-------|:---------|:----|:-----|:-------|:-------|:-----|:------|
|default_value.jpg||long|long|left|top|long*0.01||

- filepath
  - ���H���� jpg �̃p�X
- outputname
  - �o�͖�
  - `���s�����f�B���N�g��\output\outputname` �ɏo�͂����
- width, height
  - ���H��̉����A�c��
  - ���H�O���傫���l�Ȃ�Η]�����ǉ�����A�������l�Ȃ�ΐ؂�����
  - �]���̒ǉ��ӏ��� anchor_x, anchor_y �ɂ���Ďw�肷��
  - ��q�̗\���u���Ɖ��Z�@�\������
- anchor_x
  - �摜�ɗ]����ǉ�����A�������͉摜��؂���ۂɉ摜���ǂ��ɌŒ肷�邩
  - left, center, right �̂����ꂩ���w�肷��
- anchor_y
  - �摜�ɗ]����ǉ�����A�������͉摜��؂���ۂɉ摜���ǂ��ɌŒ肷�邩
  - top, center, bottom �̂����ꂩ���w�肷��
- margin
  - �㉺���E�ɒǉ������]���̕�
  - 0 �Ȃ�Η]���͒ǉ�����Ȃ�
  - ��q�̕ϐ��u���Ɖ��Z�@�\������
- comment
  - �]�������ɒǉ������R�����g�̖{��
  - �������󔒂łȂ��ꍇ�A�ꕔ�̃p�����[�^�͈ȉ��̂��̈ȊO�w��ł��Ȃ��Ȃ�
    - width: long
    - height: long
    - anchor_x: �����̉摜�̏ꍇ�� center�A�c���̉摜�̏ꍇ�� left
    - anchor_y: �����̉摜�̏ꍇ�� top�A�c���̉摜�̏ꍇ�� center

#### ���l

- filepath ���󗓂ɂ��Acomment �ɒl�����邱�ƂŃR�����g�݂̂̉摜���o�͂��邱�Ƃ��ł���
  - ���̂Ƃ� width ���w�肷��K�v������
- width, height, margin �ɂ͗\���̒u���@�\�Ɖ��Z�@�\������
  - �\���: �u����
    - long: filepath �̉摜�̒��ӂ̒���
    - short: filepath �̉摜�̒Z�ӂ̒���
    - width: filepath �̉摜�̉���
    - height: filepath �̉摜�̏c��
  - ���Z�@�\
    - `long+30` ��A`width*1.3` �̂悤�ɁA`+`, `*`, `-` ���g�����v�Z���ł���
    - ���Z�q�̊Ԃɋ󔒂�����ƃG���[���o��

### ���̑�

- �摜���c�����������𔻕ʂ��� comment ��t����B�c���������̏ꍇ�͉����Ƃ��Ĉ�����
- �ꕔ�̃G���[�ł͌����ƁA�G���[���N�������ꏊ����ĊJ���邽�߂̃R�}���h���\�������
  - ex. `python3 C:\add-caption-and-margin\add-caption-and-margin.py C:\add-caption-and-margin\csv.csv 15`
