# BeetsPlugins
 A collection of plugins for the music manager [beets](https://beets.io/).
 ### - [MusicBrainz Genres](https://github.com/mistwyrm/BeetsPlugins/blob/main/README.md#musicbrainz-genres)
 ### - [MusicBrainz Helper](https://github.com/mistwyrm/BeetsPlugins/blob/main/README.md#musicbrainz-helper)

# MusicBrainz Genres
This plugin fetches community voted genres from MusicBrainz and applies them to the albums and items in your beets library.

## Installation
Download [mbgenres.py](https://github.com/mistwyrm/BeetsPlugins/blob/main/mbgenres.py) and install it in your beets configuration. 

For instructions on installing a 3rd party beets plugin, please reference the section entitled [Other Plugins](https://docs.beets.io/en/latest/plugins/index.html#other-plugins) in the beets documentation for plugins.

## Configuration
The following configuration options can be added to your beets config file under a ```mbgenres:``` section.

- **genrecount**: The maximum number of genres to fetch for a release from MusicBrainz. Default: ```5```.
- **minvotes**: The minimum number of votes required for a genre to be added. Default: ```1```.
- **fallback**: A string to be used if no genres are found on MusicBrainz. You can set the string as ```''``` if you want genres to be cleared. ```None```, the default value, will keep existing tags even if the config option ```replace``` is set to ```True```.  Default: ```None```.
- **dynamiccount**: If set to ```True```, allows the number of genres to exceed the genrecount setting if tied votes would be excluded. This should be configured with the ```dynamicdivider``` option. If set to ```False``` then the genrecount will be strictly followed, ties will be decided by alphabetical order of tags. Default: ```True```.
- **dynamicdivider**: Used with ```dynamiccount```. Tags with vote counts greater than or equal to the dynamicdivider will be put in one group, tags with vote counts less than dynamicdivider will be put in a second group. If the maximum number of genres selected contains only genres in the first group or only in the second group, then dynamiccount will overflow any ties. If the tied votes are in the second group and there are also tags from the first group, then all of the tied genres will be removed instead of overflowed. Default: ```2```.<br>
***For more details on how ```dynamiccount``` and ```dynamicdivider``` work, see the Dynamic Count and Divider Explainer section.***
- **artistfallback**: If set to ```True```, fetches genres from the release artist if no genres are found at the release or release group level. Default: ```True```.
- **replace**: If set to ```True```, all existing genres on tracks will be replaced with MusicBrainz genres or set to the ```fallback``` value if no genres are found. If set to ```False```, the MusicBrainz genres will be added to the existing genres on albums instead of replacing them. Default: ```False```.
- **auto**: If set to ```True```, genres will be added on album imports. If set to ```False```, genres will only be added when manually run. Default: ```False```.
- **separator**: The string used to separate multiple genres. Default: ```;```.
- **titlecase**: If set to ```True```, then all genres will be title cased. If set to ```False```, all genres will be lowercased. Default: ```False```.
- **updatefrequency**: How many days between genre updates. MusicBrainz genres will not be fetched for releases that have been updated within that number of days. Use the ```-F``` or ```--force``` option when manually running to override. Default: ```7```.

### Additional Genres or Tags
By default the plugin only imports genres in [MusicBrainz's genre list](https://musicbrainz.org/genres). If you would like to whitelist other genres or tags, you can add them to the file ```tagwhitelist.txt``` in the same folder you placed the plugin in. Each whitelisted tag should be entered on its own line. ```tagwhitelist.txt``` can be manually created, or can be automatically created by running the plugin once.

## Manual Use
The plugin can be manually run with the command ```beet mbgenres [QUERY]```. If you would like to ignore the ```updatefrequency``` config setting and force a genre update, you can use the command ```beet mbgenres -F [QUERY]``` or ```beet mbgenres --force [QUERY]```.

## Dynamic Count and Divider Explainer
The purpose of the dynamic count and divider is to allow maximum count overflows in the event of vote ties, but exclude overflows of genres with low numbers of votes if higher voted genres are available. Because of the low number of genre votes on MusicBrainz, ```2``` is the recommended setting for ```dynamicdivider```, but if needed it can be set higher. Setting it to ```1``` will always allow overflows for tied votes, regardless of vote counts.

Below are some examples of how the default settings (```dynamiccount: True```, ```dynamicdivider: 2```) are applied to different scenarios.

#### Scenario 1
8 genres are returned from MusicBrainz. 6 are in the first dynamic group set by the divider, 2 are in the second dynamic group. The ```genrecount``` setting is configured to ```5```, so the overflow from the first dynamic group is allowed. <br>
**Original genres:** <br>
```'alternative rock':3, 'pop rock':2', electronic':2, 'jungle':2, 'new wave':2, 'pop':2, 'power pop':1, 'rock':1``` <br>
**Dynamic result:** <br>
```'alternative rock':3, 'pop rock':2', electronic':2, 'jungle':2, 'new wave':2, 'pop':2```

#### Scenario 2
8 genres are returned from MusicBrainz. 2 are in the first dynamic group set by the divider, 6 are in the second dynamic group. The ```genrecount``` setting is configured to ```5```, so the overflow from the second dynamic group is discarded. <br>
**Original genres:** <br>
```'alternative rock':3, 'pop rock':2', electronic':1, 'jungle':1, 'new wave':1, 'pop':1, 'power pop':1, 'rock':1``` <br>
**Dynamic result:** <br>
```'alternative rock':3, 'pop rock':2'```

#### Scenario 3
8 genres are returned from MusicBrainz. All 8 are in the second dynamic group. The ```genrecount``` setting is configured to ```5```, but the overflow is allowed as there are no genres in the first group. <br>
**Original genres:** <br>
```'alternative rock':1, 'pop rock':1', electronic':1, 'jungle':1, 'new wave':1, 'pop':1, 'power pop':1, 'rock':1``` <br>
**Dynamic result:** <br>
```'alternative rock':1, 'pop rock':1', electronic':1, 'jungle':1, 'new wave':1, 'pop':1, 'power pop':1, 'rock':1```

#### Scenario 4
4 genres are returned from MusicBrainz. 1 is in the first dynamic group set by the divider, 3 are in the second dynamic group. The ```genrecount``` setting is configured to ```5```, so no genres need to be discarded and the genres are unaltered. <br>
**Original genres:** <br>
```'alternative rock':2, 'pop rock':1, 'electronic':1, 'jungle':1``` <br>
**Dynamic result:** <br>
```'alternative rock':2, 'pop rock':1, 'electronic':1, 'jungle':1```

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