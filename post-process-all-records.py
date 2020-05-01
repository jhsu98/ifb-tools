from ifb import IFB
import time

def postprocessAllRecords(api, profile_id, page_id, step=20):
   records = api.readAllRecords(profile_id, page_id)
   
   if records:
      i = 0
      while i < len(records):
         start = i
         stop = i + step if i + step < len(records) else len(records)
         section = records[start:stop]

         try:
            api.createPageTriggerPost(profile_id, page_id, section)
         except Exception as e:
            print(e)
         else:
            print(f"Records ({start+1}-{stop}) triggered...")
         finally:
            i += step
            time.sleep(5)

if __name__ == "__main__":
   server = "acts.iformbuilder.com"
   client_key = "0b98c4482617d0fd307187e015a05f305e1bc751"
   client_secret = "bc83f91f141ae32468b372f606fb6808fa59daf8"

   api = IFB(server, client_key, client_secret)

   postprocessAllRecords(api, 2, 89285)