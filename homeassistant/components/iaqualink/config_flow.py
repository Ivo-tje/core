"""Config flow to configure zone component."""
from __future__ import annotations

from iaqualink import AqualinkClient, AqualinkLoginException
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN


class AqualinkFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Aqualink config flow."""

    VERSION = 1

    async def async_step_user(self, user_input: ConfigType | None = None):
        """Handle a flow start."""
        # Supporting a single account.
        entries = self.hass.config_entries.async_entries(DOMAIN)
        if entries:
            return self.async_abort(reason="single_instance_allowed")

        errors = {}

        if user_input is not None:
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]

            try:
                aqualink = AqualinkClient(username, password)
                await aqualink.login()
                return self.async_create_entry(title=username, data=user_input)
            except AqualinkLoginException:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_USERNAME): str, vol.Required(CONF_PASSWORD): str}
            ),
            errors=errors,
        )

    async def async_step_import(self, user_input: ConfigType | None = None):
        """Occurs when an entry is setup through config."""
        return await self.async_step_user(user_input)
