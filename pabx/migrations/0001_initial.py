# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eventtype', models.CharField(max_length=30)),
                ('eventtime', models.DateTimeField()),
                ('userdeftype', models.CharField(max_length=255)),
                ('cid_name', models.CharField(max_length=80)),
                ('cid_num', models.CharField(max_length=80)),
                ('cid_ani', models.CharField(max_length=80)),
                ('cid_rdnis', models.CharField(max_length=80)),
                ('cid_dnid', models.CharField(max_length=80)),
                ('exten', models.CharField(max_length=80)),
                ('context', models.CharField(max_length=80)),
                ('channame', models.CharField(max_length=80)),
                ('appname', models.CharField(max_length=80)),
                ('appdata', models.CharField(max_length=80)),
                ('amaflags', models.IntegerField()),
                ('accountcode', models.CharField(max_length=20)),
                ('peeraccount', models.CharField(max_length=20)),
                ('uniqueid', models.CharField(max_length=150)),
                ('linkedid', models.CharField(max_length=150)),
                ('userfield', models.CharField(max_length=255)),
                ('peer', models.CharField(max_length=80)),
                ('extra', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cel',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VwSipregs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('ipaddr', models.CharField(max_length=15)),
                ('port', models.IntegerField()),
                ('regseconds', models.IntegerField()),
                ('defaultuser', models.CharField(max_length=80)),
                ('fullcontact', models.CharField(max_length=80)),
                ('regserver', models.CharField(max_length=100, blank=True)),
                ('useragent', models.CharField(max_length=20, blank=True)),
                ('lastms', models.IntegerField()),
            ],
            options={
                'db_table': 'vw_sipregs',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='rt_calls',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Event', models.CharField(max_length=100, null=True, blank=True)),
                ('Channel', models.CharField(max_length=100, null=True, blank=True)),
                ('ChannelState', models.CharField(max_length=100)),
                ('ChannelStateDesc', models.CharField(max_length=10, null=True, blank=True)),
                ('CallerIDNum', models.IntegerField(max_length=40, null=True, blank=True)),
                ('CallerIDName', models.CharField(max_length=100)),
                ('ConnectedLineNum', models.CharField(max_length=100, null=True, blank=True)),
                ('ConnectedLineName', models.CharField(max_length=100, null=True, blank=True)),
                ('Language', models.CharField(max_length=10, null=True, blank=True)),
                ('AccountCode', models.CharField(max_length=100, null=True, blank=True)),
                ('Context', models.CharField(max_length=100, null=True, blank=True)),
                ('Exten', models.CharField(max_length=100, null=True, blank=True)),
                ('Priority', models.IntegerField(max_length=10, null=True, blank=True)),
                ('Uniqueid', models.CharField(unique=True, max_length=100)),
                ('Application', models.CharField(max_length=100, null=True, blank=True)),
                ('ApplicationData', models.CharField(max_length=100, null=True, blank=True)),
                ('Duration', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('BridgeId', models.CharField(max_length=200, unique=True, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=10)),
                ('ipaddr', models.CharField(default=b'0.0.0.0', max_length=15, blank=True)),
                ('port', models.IntegerField(default=b'5060', null=True, blank=True)),
                ('regseconds', models.IntegerField(null=True, blank=True)),
                ('defaultuser', models.CharField(max_length=10, blank=True)),
                ('fullcontact', models.CharField(max_length=250, blank=True)),
                ('regserver', models.CharField(max_length=20, blank=True)),
                ('useragent', models.CharField(max_length=50, blank=True)),
                ('lastms', models.IntegerField(null=True, blank=True)),
                ('host', models.CharField(default=b'dynamic', max_length=40, blank=True)),
                ('type', models.CharField(default=b'friend', max_length=6, blank=True, choices=[(b'friend', b'friend'), (b'user', b'user'), (b'peer', b'peer')])),
                ('context', models.CharField(default=b'default', max_length=40, blank=True)),
                ('permit', models.CharField(max_length=40, blank=True)),
                ('deny', models.CharField(max_length=40, blank=True)),
                ('secret', models.CharField(max_length=40, blank=True)),
                ('md5secret', models.CharField(max_length=40, blank=True)),
                ('remotesecret', models.CharField(max_length=40, blank=True)),
                ('transport', models.CharField(default=b'udp', max_length=7, blank=True, choices=[(b'udp', b'udp'), (b'tcp', b'tcp'), (b'udp,tcp', b'udp,tcp'), (b'tcp,udp', b'tcp,udp')])),
                ('dtmfmode', models.CharField(default=b'rfc2833', max_length=9, blank=True, choices=[(b'rfc2833', b'rfc2833'), (b'info', b'info'), (b'shortinfo', b'shortinfo'), (b'inband', b'inband'), (b'auto', b'auto')])),
                ('directmedia', models.CharField(default=b'no', max_length=6, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no'), (b'nonat', b'nonat'), (b'update', b'update')])),
                ('nat', models.CharField(default=b'no', max_length=25, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no'), (b'never', b'never'), (b'route', b'route'), (b'force_rport,comedia', b'force_port,comedia')])),
                ('callgroup', models.CharField(max_length=40, blank=True)),
                ('pickupgroup', models.CharField(max_length=40, blank=True)),
                ('language', models.CharField(max_length=40, blank=True)),
                ('allow', models.CharField(default=b'ulaw,alaw,gsm,g729', max_length=40, blank=True)),
                ('disallow', models.CharField(max_length=40, blank=True)),
                ('insecure', models.CharField(default=b'port,invite', max_length=40, blank=True)),
                ('trustrpid', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('progressinband', models.CharField(default=b'no', max_length=5, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no'), (b'never', b'never')])),
                ('promiscredir', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('useclientcode', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('accountcode', models.CharField(max_length=40, blank=True)),
                ('setvar', models.CharField(max_length=40, blank=True)),
                ('callerid', models.CharField(max_length=40, blank=True)),
                ('amaflags', models.CharField(max_length=40, blank=True)),
                ('callcounter', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('busylevel', models.IntegerField(null=True, blank=True)),
                ('allowoverlap', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('allowsubscribe', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('videosupport', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('maxcallbitrate', models.IntegerField(null=True, blank=True)),
                ('rfc2833compensate', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('mailbox', models.CharField(max_length=40, blank=True)),
                ('session_timers', models.CharField(default=b'refuse', max_length=9, blank=True, db_column=b'session-timers', choices=[(b'accept', b'accept'), (b'refuse', b'refuse'), (b'originate', b'originate')])),
                ('session_expires', models.IntegerField(null=True, db_column=b'session-expires', blank=True)),
                ('session_minse', models.IntegerField(null=True, db_column=b'session-minse', blank=True)),
                ('session_refresher', models.CharField(default=b'uac', max_length=3, blank=True, db_column=b'session-refresher', choices=[(b'uac', b'uac'), (b'uas', b'uas')])),
                ('t38pt_usertpsource', models.CharField(max_length=40, blank=True)),
                ('regexten', models.CharField(max_length=40, blank=True)),
                ('fromdomain', models.CharField(max_length=40, blank=True)),
                ('fromuser', models.CharField(max_length=40, blank=True)),
                ('qualify', models.CharField(default=b'yes', max_length=40, blank=True)),
                ('defaultip', models.CharField(max_length=40, blank=True)),
                ('rtptimeout', models.IntegerField(null=True, blank=True)),
                ('rtpholdtimeout', models.IntegerField(null=True, blank=True)),
                ('sendrpid', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('outboundproxy', models.CharField(max_length=40, blank=True)),
                ('callbackextension', models.CharField(max_length=40, blank=True)),
                ('registertrying', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('timert1', models.IntegerField(null=True, blank=True)),
                ('timerb', models.IntegerField(null=True, blank=True)),
                ('qualifyfreq', models.IntegerField(null=True, blank=True)),
                ('constantssrc', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('contactpermit', models.CharField(max_length=40, blank=True)),
                ('contactdeny', models.CharField(max_length=40, blank=True)),
                ('usereqphone', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('textsupport', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('faxdetect', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('buggymwi', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('auth', models.CharField(max_length=40, blank=True)),
                ('fullname', models.CharField(max_length=40, blank=True)),
                ('trunkname', models.CharField(max_length=40, blank=True)),
                ('cid_number', models.CharField(max_length=40, blank=True)),
                ('callingpres', models.CharField(default=b'allowed', max_length=21, blank=True, choices=[(b'allwoed_not_screened', b'allwoed_not_screened'), (b'allwoed_passed_screen', b'allwoed_passed_screen'), (b'allowed_failed_screen', b'allowed_failed_screen'), (b'allowed', b'allowed'), (b'prohib_not_screened', b'prohib_not_screened'), (b'prohib_passed_screen', b'prohib_passed_screen'), (b'prohib_failed_screen', b'prohib_failed_screen'), (b'prohib', b'prohib')])),
                ('mohinterpret', models.CharField(max_length=40, blank=True)),
                ('mohsuggest', models.CharField(max_length=40, blank=True)),
                ('parkinglot', models.CharField(max_length=40, blank=True)),
                ('hasvoicemail', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('subscribemwi', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('vmexten', models.CharField(max_length=40, blank=True)),
                ('autoframing', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('rtpkeepalive', models.IntegerField(null=True, blank=True)),
                ('call_limit', models.IntegerField(null=True, db_column=b'call-limit', blank=True)),
                ('g726nonstandard', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('ignoresdpversion', models.CharField(default=b'no', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('allowtransfer', models.CharField(default=b'yes', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
                ('dynamic', models.CharField(default=b'yes', max_length=3, blank=True, choices=[(b'yes', b'yes'), (b'no', b'no')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
