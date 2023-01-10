rule twilio_api_key : twilio secret {
    meta:
        description = "Detects a Twilio API token"
    strings:
        $ = /SK[0-9a-fA-F]{32}/
    condition:
        all of them
}