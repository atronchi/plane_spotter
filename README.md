# Plane Spotter
* Use ADS-B receivers to locate nearby aircraft.
* Use GPYES to find current location.
* Determine azimuth/elevation to a chosen aircraft.
* Actuate stepper motors on telescope mount to actively track the plane.

## Hardware
* [Raspberry pi 4](https://www.amazon.com/Raspberry-Model-2019-Quad-Bluetooth/dp/B07TD42S27) ($45)
* [Nooelec nano 3 ADS-B receivers](https://www.amazon.com/Dual-Band-NESDR-Nano-Bundle/dp/B076GWF6FF/ref=pd_sbs_147_4/133-0746579-1054605?_encoding=UTF8&pd_rd_i=B076GWF6FF&pd_rd_r=bdf3b34b-efc3-41f1-baac-4d709b651036&pd_rd_w=qcI1o&pd_rd_wg=rGVIs&pf_rd_p=12b8d3e2-e203-4b23-a8bc-68a7d2806477&pf_rd_r=CXWWHSKGPDVQS05SS261&psc=1&refRID=CXWWHSKGPDVQS05SS261) ($65)
* [GPYES2](https://www.amazon.com/Stratux-GPYes-2-0-u-blox-unit/dp/B0716BK5NT) ($16)
* [Waveshare stepper motor hat](https://www.waveshare.com/wiki/Stepper_Motor_HAT) ($19) with two 3ft RJ11 cables to connect to motors ($5)
    * motors are bi-polar steppers with 100x reduction gearing
* [stratux AHRS](https://www.amazon.com/gp/product/B06ZZCHBHT/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1) ($15)
* [Celestron Omni XLT150 telescope on a CG-4 equatorial mount](https://www.amazon.com/Celestron-Omni-XLT-150-Telescope/dp/B000NMOIP8) ($540) with [93522 dual motor drive](https://www.amazon.com/Celestron-93522-Motor-Drive-Advanced/dp/B0000C3WBB) ($140)
* [12V DC power](https://www.amazon.com/dp/B07XP6DBCR/ref=sspa_dk_detail_1?psc=1&pd_rd_i=B07XP6DBCR&pd_rd_w=um5hx&pf_rd_p=48d372c1-f7e1-4b8b-9d02-4bd86f5158c5&pd_rd_wg=9EYJO&pf_rd_r=BGRY8SWX1B97AEEE8NB4&pd_rd_r=b1ef7aa1-b2cc-4857-9258-be8572266f8d&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyUUVGQ0E1WTFFTlpOJmVuY3J5cHRlZElkPUEwMTE0NzQyMkFUNjRMRkY2ODZXOCZlbmNyeXB0ZWRBZElkPUEwMjQzNjI4V1A0VDBSRzBHM1VIJndpZGdldE5hbWU9c3BfZGV0YWlsJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==) ($15)

## Software
* dump1090 to retrieve ADS-B data
* azel.py to calculate azimuth and elevation

## TODOs
* stream-process ADS-B and GPYES2 to select an aircraft
    * selection heuristic: distance >20nm and closing, altitude >10k ft, slew rate within motor capacity
* use a kalman filter with AHRS and stepper motors to align the telescope to selected aircraft
* autofocus?


## Install dependencies
[Setup rtl-sdr](https://www.rtl-sdr.com/tag/install-guide/)
sudo apt-get install -y rtl-sdr libusb-1.0-0-dev git cmake
git clone git://git.osmocom.org/rtl-sdr.git
mkdir rtl-sdr/build
cd rtl-sdr/build
cmake ../ -DINSTALL_UDEV_RULES=ON
sudo cp ../rtl-sdr.rules /etc/udev/rules.d/
sudo ldconfig
echo 'blacklist dvb_usb_rtl28xxu' | sudo tee --append /etc/modprobe.d/blacklist-dvb_usb_rtl28xxu.conf


[From flight aware](https://flightaware.com/adsb/piaware/install)
    wget https://flightaware.com/adsb/piaware/files/packages/pool/piaware/p/piaware-support/piaware-repository_3.8.1_all.deb
    sudo dpkg -i piaware-repository_3.8.1_all.deb
    sudo apt-get update && sudo apt-get install -y piaware dump1090-fa dump978-fa

    sudo dump1090-fa --device stx:1090:0
    sudo dump978-fa --sdr driver=rtlsdr,serial=00000978  --json-stdout
