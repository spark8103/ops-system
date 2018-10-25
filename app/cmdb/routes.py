from flask import render_template, redirect, request, url_for, flash, jsonify
from flask_security import login_required
from app import db, flash_errors
from app.cmdb import bp
from app.cmdb.forms import AddSoftwareForm, EditSoftwareForm, AddIdcForm, EditIdcForm, AddServerForm, EditServerForm
from app.models import Software, Idc, Server


# software
@bp.route('/software')
@login_required
def software():
    add_software_form = AddSoftwareForm()
    edit_software_form = EditSoftwareForm()
    return render_template('cmdb/software.html', add_software_form=add_software_form,
                           edit_software_form=edit_software_form)


@bp.route('/software-list')
@login_required
def software_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    data = Software.to_collection_dict(Software.query, page, per_page, 'cmdb.software_list')
    return jsonify(data)


@bp.route('/software-add', methods=['POST'])
@login_required
def software_add():
    form = AddSoftwareForm(data=request.get_json())
    if form.validate_on_submit():
        software = Software(name=form.name.data, description=form.description.data)
        db.session.add(software)
        db.session.commit()
        flash('%s is add.' % form.name.data, 'success')
    else:
        flash_errors(form)
    return redirect(url_for('.software'))


@bp.route('/software-edit', methods=['POST'])
@login_required
def software_edit():
    id = request.form.get('e_id')
    software = Software.query.get_or_404(id)
    form = EditSoftwareForm(id=id)
    t_name = Software.query.filter_by(id=id).first().name
    if t_name is not None and t_name != form.e_name.data:
        flash("%s already in use, not change." % form.e_name.data, 'warning')
    elif form.validate_on_submit():
        software.name = form.e_name.data
        software.description = form.e_description.data
        db.session.add(software)
        flash('%s is update.' % t_name, "success")
    else:
        flash_errors(form)
    return redirect(url_for('.software'))


@bp.route('/software-del', methods=['POST'])
@login_required
def software_del():
    id = request.form.get('id')
    software = Software.query.filter_by(id=id).first()
    if software is None:
        flash('Non-existent name: %s' % request.form.get('name'), 'warning')
    else:
        db.session.delete(software)
        db.session.commit()
        flash('%s is del.' % request.form.get('name'), 'success')
    return redirect(url_for('.software'))


# idc
@bp.route('/idc')
@login_required
def idc():
    add_idc_form = AddIdcForm()
    edit_idc_form = EditIdcForm()
    return render_template('cmdb/idc.html', add_idc_form=add_idc_form,
                           edit_idc_form=edit_idc_form)


@bp.route('/idc-list')
@login_required
def idc_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    data = Idc.to_collection_dict(Idc.query, page, per_page, 'cmdb.idc_list')
    return jsonify(data)


@bp.route('/idc-add', methods=['POST'])
@login_required
def idc_add():
    form = AddIdcForm(data=request.get_json())
    if form.validate_on_submit():
        idc = Idc(name=form.name.data, zone=form.zone.data, region=form.region.data, description=form.description.data)
        db.session.add(idc)
        db.session.commit()
        flash('%s is add.' % form.name.data, 'success')
    else:
        flash_errors(form)
    return redirect(url_for('.idc'))


@bp.route('/idc-edit', methods=['POST'])
@login_required
def idc_edit():
    id = request.form.get('e_id')
    idc = Idc.query.get_or_404(id)
    form = EditIdcForm(id=id)
    t_name = Idc.query.filter_by(id=id).first().name
    if t_name is not None and t_name != form.e_name.data:
        flash("%s already in use, not change." % form.e_name.data, 'warning')
    elif form.validate_on_submit():
        idc.name = form.e_name.data
        idc.zone = form.e_zone.data
        idc.region = form.e_region.data
        idc.description = form.e_description.data
        db.session.add(idc)
        flash('%s is update.' % t_name, "success")
    else:
        flash_errors(form)
    return redirect(url_for('.idc'))


@bp.route('/idc-del', methods=['POST'])
@login_required
def idc_del():
    id = request.form.get('id')
    idc = Idc.query.filter_by(id=id).first()
    if idc is None:
        flash('Non-existent name: %s' % request.form.get('name'), 'warning')
    else:
        db.session.delete(idc)
        db.session.commit()
        flash('%s is del.' % request.form.get('name'), 'success')
    return redirect(url_for('.idc'))


# server
@bp.route('/server')
@login_required
def server():
    add_server_form = AddServerForm()
    edit_server_form = EditServerForm()
    return render_template('cmdb/server.html', add_server_form=add_server_form,
                           edit_server_form=edit_server_form)


@bp.route('/server-list')
@login_required
def server_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    data = Server.to_collection_dict(Server.query, page, per_page, 'cmdb.server_list')
    return jsonify(data)


@bp.route('/server-add', methods=['POST'])
@login_required
def server_add():
    form = AddServerForm(data=request.get_json())
    if form.validate_on_submit():
        server = Server(name=form.name.data, idc=form.idc.data, instance_id=form.instance_id.data,
                     instance_type=form.instance_type.data, platform=form.platform.data,
                     image_name=form.image_name.data, key_name=form.key_name.data, private_ip=form.private_ip.data,
                     public_ip=form.public_ip.data, block_device=form.block_device.data, subnet=form.subnet.data,
                     create_time=form.create_time.data, category=form.category.data,
                     category_branch=form.category_branch.data, status=form.status.data,
                     description=form.description.data)
        db.session.add(server)
        db.session.commit()
        flash('%s is add.' % form.name.data, 'success')
    else:
        flash_errors(form)
    return redirect(url_for('.server'))


@bp.route('/server-edit', methods=['POST'])
@login_required
def server_edit():
    id = request.form.get('e_id')
    server = Server.query.get_or_404(id)
    form = EditServerForm(id=id)
    t_name = Server.query.filter_by(id=id).first().name
    if t_name is not None and t_name != form.e_name.data:
        flash("%s already in use, not change." % form.e_name.data, 'warning')
    elif form.validate_on_submit():
        server.name = form.e_name.data
        server.idc = form.e_idc.data
        server.instance_id = form.e_instance_id.data
        server.instance_type = form.e_instance_type
        server.platform = form.e_platform
        server.image_name = form.e_image_name
        server.key_name = form.e_key_name
        server.private_ip = form.e_private_ip
        server.public_ip = form.e_public_ip
        server.block_device = form.e_block_device
        server.subnet = form.e_subnet
        server.create_time = form.e_create_time
        server.category = form.e_category
        server.category_branch = form.e_category_branch
        server.status = form.e_status
        server.description = form.e_description.data
        db.session.add(server)
        flash('%s is update.' % t_name, "success")
    else:
        flash_errors(form)
    return redirect(url_for('.server'))


@bp.route('/server-del', methods=['POST'])
@login_required
def server_del():
    id = request.form.get('id')
    server = Server.query.filter_by(id=id).first()
    if server is None:
        flash('Non-existent name: %s' % request.form.get('name'), 'warning')
    else:
        db.session.delete(server)
        db.session.commit()
        flash('%s is del.' % request.form.get('name'), 'success')
    return redirect(url_for('.server'))
