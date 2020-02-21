import os
import flask
from wtforms import RadioField, SubmitField
from flask_wtf import FlaskForm

from deployment import deploy

SECRET_KEY = "dev"

app = flask.Flask(__name__,static_folder="./static")
app.config.from_object(__name__)

class PayloadSelection(FlaskForm):
    ''' Class that abstracts the creation of an HTML form.
    The SubmitField method creates a submit button and returns
    a boolean value for each of the various payload types.'''

    arm_karma  = SubmitField("ARM Devices")
    arm_jammer = SubmitField("ARM Devices")
    arm_io     = SubmitField("ARM Devices")
    arm_cam    = SubmitField("ARM Devices")
    arm_geo    = SubmitField("ARM Devices")
    arm_hail   = SubmitField("ARM Devices")

# flask decorator to wrap a function with a route that will
# catch the requested uri and redirect it to the return 
@app.route('/', methods=["GET","POST"])
def home():
    ''' Function that handles all page interaction. Renders the
    page based off of templating. Allows us to detect the payload
    selection and kick off the deployment scripts. '''

    # instantiate all payload selection buttons/forms
    form = PayloadSelection()

    if form.validate_on_submit():
        if form.arm_karma.data:
            payload = "setup.cfg.karma"
            config  = "/home/pi/P4wnp1/setup.cfg"
            choice = "KARMA"
        elif form.arm_jammer.data:
            payload = "rc.local"
            config = "/etc/rc.local"
            payload2 = "setup.cfg.deauth"
            config2 = "/home/pi/P4wnp1/setup.cfg"
            choice = "WiFi Jamming"
        elif form.arm_io.data:
            payload = "setup.cfg.io"
            config  = "/home/pi/P4wnp1/setup.cfg"
            choice = "IO Message"
        elif form.arm_cam.data:
            payload = "setup.cfg.camera"
            config  = "/home/pi/P4wnp1/setup.cfg"
            choice = "Webcam Disruption"
        elif form.arm_geo.data:
            payload = "setup.cfg.geo"
            config  = "/home/pi/P4wnp1/setup.cfg"
            choice = "Geolocate"
        elif form.arm_hail.data:
            payload = "setup.cfg.hailmary"
            config  = "/home/pi/P4wnp1/setup.cfg"
            choice = "Hail Mary"

        if payload2:
            deploy(payload2,config2)
        failures = deploy(payload,config)
        failed = str(len(failures)) + "." + "".join(failures)
        return flask.render_template("armed.html", failed=failed, choice=choice)

    '''
    # handle submit button press and launch script
    if karma.validate_on_submit():
        if karma.arm_karma.data:
            print(os.system("ls"))

    if jammer.validate_on_submit():
        if jammer.arm_jammer.data:
            print(os.system("ps"))
            return flask.render_template("armed.html")

    if io.validate_on_submit():
        if io.arm_io.data:
            print(os.system("ps"))

    if cam_disrupt.validate_on_submit():
        if cam_disrupt.arm_cam.data:
            print(os.system("ps"))

    if geolocate.validate_on_submit():
        if geolocate.arm_geo.data:
            print(os.system("ps"))
    '''

    return flask.render_template("index.html", form=form)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=80)
