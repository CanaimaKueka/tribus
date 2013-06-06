{% import "macros.html" as macros %}
{% include "tags/header.html" %}
{% if tag_list_type == 'list' %}
    {% if not tags.object_list %}
        <span>{% trans %}Nothing found{% endtrans %}</span>
    {% endif %}
    {% if tags.object_list %}
        <div class='clearfix'></div>
        <ul class='tags'>
            {% for tag in tags.object_list %}
            <li>
                {{ macros.tag_widget(
                            tag=tag.name,
                            html_tag='div',
                            truncate_long_tag=True,
                            extra_content='<span class="tag-number">&#215; ' ~
                                            tag.used_count|intcomma ~ '</span>'
                    )
                }}
            </li>
            {% endfor %}
        </ul>
        <div class="clean"></div>
        <div class="pager">
            {{macros.paginator(paginator_context)}}
        </div>
    {% endif %}
{% else %}
    <div class="clearfix"></div>
    {% if not tags %}
        <span>{% trans %}Nothing found{% endtrans %}</span>
    {% endif %}
    {{ macros.tag_cloud(tags=tags, font_sizes=font_size, search_state=search_state) }}
{% endif %}
