FROM ubuntu:18.04
ADD walnut /walnut/
ADD walnut-vue/dist /walnut-vue
RUN mkdir /root/.pip
RUN cp /walnut/sources.list /etc/apt/sources.list && \
    apt-get update && \
    apt-get install python3 python3-pip nginx -y && \
    cp /walnut/pip.conf /root/.pip/pip.conf
RUN pip3 install -r /walnut/requirements.txt && \
    mv /walnut/run.sh /run.sh && \
    chmod +x /run.sh && \
    /bin/cp -f /walnut/nginx.conf /etc/nginx/nginx.conf
ENV ldap_user xxxxxx
ENV ldap_password xxxxxx
ENV ldap_host xxxxx
ENV ldap_search_base xxxxx
ENV vpn_status_log /tmp/openvpn-status.log

ENV aliyun_sms_app_key xxxxxx
ENV aliyun_sms_app_secret xxxxx
ENV aliyun_sms_sign_name xxxx
ENV aliyun_sms_template_code xxxxx
ENTRYPOINT ["/run.sh"]
EXPOSE 8000
VOLUME ["/walnut/db"]
