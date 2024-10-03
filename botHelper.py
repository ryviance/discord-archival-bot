# Helper functions

async def send_in_chunks(interaction, message):
    # Used to circumvent discord message limit
    # Helper for /archive
    lines = message.splitlines()
    chunk = ""

    for line in lines:
        # Check if adding the line will exceed the character limit
        if len(chunk) + len(line) + 1 > 2000:
            # Send the current chunk before adding the new line
            await interaction.followup.send(chunk)
            chunk = ""

        # Add the line to the chunk
        if chunk:
            chunk += "\n" + line
        else:
            chunk = line

    # Send any remaining chunk
    if chunk:
        await interaction.followup.send(chunk)