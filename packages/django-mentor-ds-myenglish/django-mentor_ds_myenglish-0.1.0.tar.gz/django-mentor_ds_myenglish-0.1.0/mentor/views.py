from django.shortcuts import render
from util_demian import utils
from .forms import AppointmentForm
from _data import contents

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


def home(request, lang=None):
    """
    컨텍스트를 이곳에서 만들지 않고 _data 폴더의 contents.py에서 만들어진 것을 가져다 쓴다.
    """
    if lang == 'kor':
        c = contents.context_kor
        c['lang']['selected'] = 'kor'
    elif lang == 'eng':
        c = contents.context_eng
        c['lang']['selected'] = 'eng'
    else:
        # 페이지 로딩시 초기 언어
        c = contents.context_eng
        c['lang']['selected'] = 'eng'

    logger.debug(c)
    if request.method == 'GET':
        return render(request, 'mentor/index.html', c)
    elif request.method == "POST":
        c.update(make_post_context(request.POST, c['basic_info']['consult_email']))
        return render(request, 'mentor/index.html', c)


def make_post_context(request_post, consult_mail, anchor='appointment'):
    logger.info(request_post)
    context = {}
    # appointment 앱에서 post 요청을 처리함.
    logger.info(f'request.POST : {request_post}')
    form = AppointmentForm(request_post)
    # 템플릿 렌더링 후 바로 appointment 앵커로 이동시키기 위해 설정
    context['anchor'] = anchor
    if form.is_valid():
        name = form.cleaned_data['name']
        phone = form.cleaned_data['phone']
        date = form.cleaned_data['date']
        message = form.cleaned_data['message']
        logger.info(f'Pass validation test -  {name} {phone} {date} {message}')
        is_sendmail = utils.mail_to(title=f'{name} 고객 상담 문의',
                                    text=f'이름: {name}\n연락처: {phone}\n예약일: {date}\n메시지: {message}',
                                    mail_addr=consult_mail)
        if is_sendmail:
            context['post_message'] = '담당자에게 예약신청이 전달되었습니다. 확인 후 바로 연락드리겠습니다. 감사합니다.'
        else:
            context['post_message'] = '메일 전송에서 오류가 발생하였습니다. 카카오톡이나 전화로 문의주시면 감사하겠습니다. 죄송합니다.'
        return context
    else:
        logger.error('Fail form validation test')
        context['post_message'] = '입력 항목이 유효하지 않습니다. 다시 입력해 주십시요.'
        return context
