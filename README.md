# BeetsPlugins
 A collection of plugins for the music manager "beets".

# MusicBrainz Helper
This plugin generates an HTML report of your beets library that can be helpful for MusicBrainz editing.

## Prerequisites: 
- Your library must be accurately linked to MusicBrainz releases. **If your recordings are not linked to the correct releases, then this plugin will not generate accurate data and should not be used.** 
- Your beets installation must have the [Chromaprint/Acoustid plugin](https://beets.readthedocs.io/en/stable/plugins/chroma.html) installed and you must use the plugin to fingerprint and submit your files to Acoustid before using this plugin. 
- Installing and running the [mbsync plugin](https://docs.beets.io/en/latest/plugins/mbsync.html) is highly recommended to make sure you are generating a report from the most recent MusicBrainz data. 

## Installation
Download [mbhelperplugin.py](https://github.com/mistwyrm/BeetsPlugins/blob/main/mbhelperplugin.py) and install it in your beets configuration. 

For instructions on installing a 3rd party beets plugin, please reference the section entitled [Other Plugins](https://docs.beets.io/en/latest/plugins/index.html#other-plugins) in the beets documentation for plugins.

## Instructions
Run the command `beets mbhelper` to generate an html file containing the MusicBrainz Helper report. `-d DIRECTORY` or `--directory DIRECTORY` can be used as arguments if you would like to specify a directory path for the file to be placed in.

The HTML report contains two pages, you can switch between these pages using the menu in the top right.

### Recordings with Shared Acoustids
This page lists tracks in your library that are linked to different MusicBrainz recordings but share the same acoustid. This may indicate that the recordings should be merged.

Shared acoustids are a good sign that recordings may need to be merged, but should not be the only thing you rely on. Acoustids group similar fingerprints and may sometimes group recordings that should remain separate in MusicBrainz (examples are clean vs explicit recordings, DJ mixes, or differences in intros or outros).

### Recordings With Multiple Acoustids
This page lists tracks in your library that share MusicBrainz recordings but do not have matching acoustids. This may indicate a mistaken recording merge in the past that needs to be split. 

**This list has a very high false positive rate.** Differences in the speed of a recording, added noise (such as from a vinyl rip), or other small differences between releases can cause the same recording to have multiple acoustids. Please review the acoustids individually on acoustid.org (the fingerprint comparison tool is good for this purpose) and use common sense before splitting a recording.