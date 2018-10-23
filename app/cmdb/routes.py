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
        flash('%s is add.' % request.form.get('name'), 'success')
    else:
        flash_errors(form)
    return redirect(url_for('.software'))


@bp.route('/software-edit', methods=['POST'])
@login_required
def software_edit():
    id = request.form.get('e_id')
    software = Software.query.get_or_404(id)
    form = EditSoftwareForm(id=id)
    if Software.query.filter_by(name=form.e_name.data).first() is not None:
        flash("%s already in use." % form.e_name.data, 'warning')
    elif form.validate_on_submit():
        software.name = form.e_name.data
        software.description = form.e_description.data
        db.session.add(software)
        flash('%s is update.' % request.form.get('e_name'), "success")
    else:
        flash_errors(form)
    return redirect(url_for('.software'))


@bp.route('/software-del', methods=['POST'])
@login_required
def software_del():
    id = request.form.get('id')
    software = Software.query.filter_by(id=id).first()
    if software is None:
        flash('Non-existent software: %s' % request.form.get('name'), 'warning')
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
    data = Software.to_collection_dict(Idc.query, page, per_page, 'cmdb.idc_list')
    return jsonify(data)


@bp.route('/idc-add', methods=['POST'])
@login_required
def idc_add():
    form = AddIdcForm(data=request.get_json())
    if form.validate_on_submit():
        idc = Idc(name=form.name.data, zone=form.zone.data, region=form.region.data, description=form.description.data)
        db.session.add(idc)
        db.session.commit()
        flash('%s is add.' % request.form.get('name'), 'success')
    else:
        flash_errors(form)
    return redirect(url_for('.idc'))


@bp.route('/idc-edit', methods=['POST'])
@login_required
def idc_edit():
    id = request.form.get('e_id')
    idc = Idc.query.get_or_404(id)
    form = EditIdcForm(id=id)
    if Idc.query.filter_by(name=form.e_name.data).first() is not None:
        flash("%s already in use." % form.e_name.data, 'warning')
    elif form.validate_on_submit():
        idc.name = form.e_name.data
        idc.zone = form.e_zone.data
        idc.region = form.e_region.data
        idc.description = form.e_description.data
        db.session.add(idc)
        flash('%s is update.' % request.form.get('e_name'), "success")
    else:
        flash_errors(form)
    return redirect(url_for('.idc'))


@bp.route('/idc-del', methods=['POST'])
@login_required
def idc_del():
    id = request.form.get('id')
    idc = Idc.query.filter_by(id=id).first()
    if idc is None:
        flash('Non-existent software: %s' % request.form.get('name'), 'warning')
    else:
        db.session.delete(idc)
        db.session.commit()
        flash('%s is del.' % request.form.get('name'), 'success')
    return redirect(url_for('.idc'))


# server
