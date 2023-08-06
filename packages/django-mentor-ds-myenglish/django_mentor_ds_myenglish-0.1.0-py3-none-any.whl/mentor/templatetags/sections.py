from django.template import Library, loader
from ..forms import AppointmentForm
from django.contrib.staticfiles import finders
import os

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


register = Library()

# https://localcoder.org/django-inclusion-tag-with-configurable-template


@register.simple_tag(takes_context=True)
def hero(context):
    t = loader.get_template("mentor/_hero.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def contact(context):
    """
    contact 내부에서 appointment를 처리한다.
    """
    t = loader.get_template("mentor/_contact.html")
    context.update({
        'form': AppointmentForm(),
        'post_message': context.get('post_message', None),
        'naver_link': context.get('naver', None),
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def about(context):
    t = loader.get_template("mentor/_about.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def counts(context):
    t = loader.get_template("mentor/_counts.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def whyus(context):
    t = loader.get_template("mentor/_whyus.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def features(context):
    t = loader.get_template("mentor/_features.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def courses(context):
    t = loader.get_template("mentor/_courses.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def trainers(context):
    t = loader.get_template("mentor/_trainers.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def intro(context):
    t = loader.get_template("mentor/_intro.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def testimonials(context):
    t = loader.get_template("mentor/_testimonials.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def faq(context):
    t = loader.get_template("mentor/_faq.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())