from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
import asyncio, json, time, pathlib
temp= pathlib.Path(r"Z:\PROJECT ZHOPA\goosecool1-s_ST-MHP-PD\ProtoOnYourScreen!\src\environment\winsdk_audio_temp.json")

async def getMediaInfo():
    try:
        if not (manager:= await MediaManager.request_async()):             return None
        if not (session:= manager.get_current_session()):                  return {"status": "no_session"}
        if not (props  := await session.try_get_media_properties_async()): return {"status": "no_properties"}
        pbi= session.get_playback_info();       status = pbi.playback_status if pbi is not None else "unknown"
        media_data = {
            "status": "playing" if status == 4 else "paused",
            "title": props.title or "Unknown",
            "artist": props.artist or "Unknown",
            "album": props.album_title or "Unknown",
            "timestamp": time.time(),
            "genres": list(props.genres) if props.genres else []
        }; return media_data
    except Exception as e: return {"status":"Oh...I have some problem... O-O||", "error":str(f"{e} \n Mmmph~...")}

async def updateJson():
    lastData = None
    while True:
        try:
            if (info:= await getMediaInfo()) !=lastData:
                with open(temp, 'w', encoding='utf-8') as f: json.dump(info, f, ensure_ascii=False, indent=2); lastData = info
            await asyncio.sleep(1)
        except Exception as e: await asyncio.sleep(5)
if __name__ == "__main__": asyncio.run(updateJson())