import logging
from flask import redirect, render_template, request, url_for, flash
from flask import current_app as app
from flask_login import login_required, current_user

from cryptoadvance.specter.specter import Specter
from cryptoadvance.specter.services.controller import user_secret_decrypted_required
from cryptoadvance.specter.user import User
from cryptoadvance.specter.wallet import Wallet
from cryptoadvance.specter.commands.psbt_creator import PsbtCreator
from embit.liquid.networks import get_network
from .service import ExfundService
from .util import parse_csv

logger = logging.getLogger(__name__)

exfund_endpoint = ExfundService.blueprint


def ext() -> ExfundService:
    """convenience for getting the extension-object"""
    return app.specter.ext["exfund"]


def specter() -> Specter:
    """convenience for getting the specter-object"""
    return app.specter


@exfund_endpoint.route("/", methods=["GET", "POST"])
def index():
    user = app.specter.user_manager.get_user()
    show_menu = ExfundService.id in user.services

    wallet_names = sorted(current_user.wallet_manager.wallets.keys())
    wallets = [current_user.wallet_manager.wallets[name] for name in wallet_names]
    rawcsv = ""
    try:
        if request.method == "POST":
            action = request.form["action"]
            if action == "settings":
                show_menu = request.form.get("show_menu")
                if show_menu:
                    user.add_service(ExfundService.id)
                else:
                    user.remove_service(ExfundService.id)
            elif action == "parse":
                rawcsv = request.form.get("rawcsv", "")
                addresses, chain, invalid_lines = parse_csv(rawcsv)
                expected_net = get_network(app.specter.chain)
                net = get_network(chain)
                if net != expected_net:
                    raise ValueError(
                        f"Invalid chain: {chain}, expected: {app.specter.chain}"
                    )
                if invalid_lines:
                    flash(f"{len(invalid_lines)} lines couldn't be parsed")
                assets = set().union(*[wallet.balance.get("assets",{}).keys() for wallet in wallets])
                assets = [app.specter.default_asset]+list(assets)
                return render_template(
                    "exfund/table.jinja",
                    wallets=wallets,
                    addresses=addresses,
                    is_liquid=app.specter.is_liquid,
                    assets=assets,
                )
            elif action == "createpsbt":
                wallet_alias = request.form.get("source_wallet")
                wallet = current_user.wallet_manager.wallets[wallet_alias]
                addresses = request.form.getlist("addresses[]")
                labels = request.form.getlist("labels[]")
                amounts = request.form.getlist("amounts[]")
                if app.specter.is_liquid:
                    assets = request.form.getlist("assets[]")
                    scales = [1e-8 if a.endswith("-sat") else 1 for a in assets]
                    # remove -sat part
                    assets = [a.split("-")[0] for a in assets]
                else:
                    assets = ["btc" for a in addresses]
                    scales = [1e-8 if u == "sat" else 1 for u in request.form.getlist("units[]")]
                obj = {
                    "fee_option": request.form.get("fee_option", "dynamic"),
                    "fee_rate": request.form.get("fee_rate", "1"),
                    "fee_rate_dynamic": request.form.get("fee_rate_dynamic", "1"),
                    "rbf": request.form.get("rbf", True),
                }
                for i, (addr, label, amount, asset, scale) in enumerate(
                    zip(addresses, labels, amounts, assets, scales)
                ):
                    obj[f"address_{i}"] = addr
                    obj[f"label_{i}"] = label
                    obj[f"btc_amount_{i}"] = round(float(amount) * scale, 8)
                    obj[f"amount_unit_{i}"] = asset
                psbt_creator = PsbtCreator(app.specter, wallet, "ui", request_form=obj)
                psbt = psbt_creator.create_psbt(wallet)
                return render_template(
                    "wallet/send/sign/wallet_send_sign_psbt.jinja",
                    psbt=psbt,
                    labels=labels,
                    wallet_alias=wallet_alias,
                    wallet=wallet,
                    specter=app.specter,
                    rand=0,
                )
            else:
                flash(f"Wrong action {action}", "error")
    except Exception as e:
        flash(f"Server error: {e}", "error")
    return render_template(
        "exfund/index.jinja",
        wallets=wallets,
        show_menu=show_menu,
        rawcsv=rawcsv,
    )
