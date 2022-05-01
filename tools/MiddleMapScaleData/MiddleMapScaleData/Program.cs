using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MiddleMapScaleData
{
    internal class Program
    {
        static void Main(string[] args)
        {
            JObject ret = new JObject();
            MiddleMap.Init(@"E:\\Extracted");
            foreach (MiddleMapPosData map in MiddleMap.GetAll())
            {
                if (!ret.ContainsKey(map.ID.ToString()))
                    ret[map.ID.ToString()] = new JObject();
                ((JObject)ret[map.ID.ToString()]).Add(map.SubMapID.ToString(), JObject.FromObject(map));
            }
            File.WriteAllText("../../../../../output/MapScales.json", ret.ToString(Formatting.Indented), new UTF8Encoding(false));
        }
    }
}
