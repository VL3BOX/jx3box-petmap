using CsvHelper;
using CsvHelper.Configuration;
using IniParser;
using IniParser.Model;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace MiddleMapScaleData
{
    internal class MiddleMapPosData
    {
        [JsonIgnore]
        public int ID { get; private set; }
        [JsonIgnore]
        public int SubMapID { get; private set; }
        [JsonProperty]
        public string Name { get; private set; }
        [JsonProperty]
        public decimal Width { get; private set; }
        [JsonProperty]
        public decimal Height { get; private set; }
        [JsonProperty]
        public decimal Scale { get; private set; }
        [JsonProperty]
        public decimal StartX { get; private set; }
        [JsonProperty]
        public decimal StartY { get; private set; }

        public (int x, int y) GetRelativePos(int x, int y)
        {
            int actualX = (int)((x - this.StartX) * this.Scale);
            // 中地图左下角为坐标零点，Y 轴需要反转
            int actualY = (int)(this.Height - ((y - this.StartY) * this.Scale));
            return (actualX, actualY);
        }

        public MiddleMapPosData(int id, int subMapId, string name, decimal width, decimal height, decimal scale, decimal startX, decimal startY)
        {
            this.ID = id;
            this.SubMapID = subMapId;
            this.Name = name;
            this.Width = width;
            this.Height = height;
            this.Scale = scale;
            this.StartX = startX;
            this.StartY = startY;
        }
    }

    internal class MiddleMap
    {
        private static Regex middleMapSection = new Regex("^middlemap(\\d+)$", RegexOptions.Singleline | RegexOptions.Compiled);

        private static Dictionary<(int mapID, int subMapID), MiddleMapPosData> middleMapInfoMaster;

        private static Dictionary<int, string> GetAllMapsFromTab(string path)
        {
            Dictionary<int, string> ret = new Dictionary<int, string>();
            using (var stream = new StreamReader(path, Encoding.GetEncoding(936)))
            {
                using (var csvReader = new CsvReader(stream,
                    new CsvConfiguration(CultureInfo.InvariantCulture)
                    {
                        Delimiter = "\t",
                        Encoding = Encoding.GetEncoding(936),
                        HasHeaderRecord = true
                    }))
                {
                    csvReader.Read();
                    csvReader.ReadHeader();
                    while (csvReader.Read())
                    {
                        int id = int.Parse(csvReader.GetField("ID"));
                        string name = csvReader.GetField("Name");
                        ret[id] = name;

                    }
                }
            }
            return ret;
        }

        public static Dictionary<int, KeyDataCollection> GetMiddleMapsFromIni(string path)
        {
            IniData ini = new FileIniDataParser().ReadFile(path, Encoding.GetEncoding(936));
            Dictionary<int, KeyDataCollection> middleMaps = new Dictionary<int, KeyDataCollection>();
            foreach (var section in ini.Sections)
            {
                Match match = middleMapSection.Match(section.SectionName);
                if (match.Success)
                {
                    middleMaps.Add(int.Parse(match.Groups[1].Value), section.Keys);
                }
            }
            return middleMaps;
        }

        public static void Init(string basePath)
        {
            middleMapInfoMaster = new Dictionary<(int mapID, int subMapID), MiddleMapPosData>();
            var allMaps = GetAllMapsFromTab(new FileInfo(Path.Combine(basePath, @"settings\MapList.tab")).FullName);
            foreach (var map in allMaps)
            {
                FileInfo configFile = new FileInfo(Path.Combine(new DirectoryInfo(Path.Combine(basePath, @"data\source\maps\")).FullName, $@"{map.Value}minimap\config.ini"));
                if (configFile.Exists)
                {
                    var subMaps = GetMiddleMapsFromIni(configFile.FullName);
                    foreach (var subMap in subMaps)
                    {
                        var mapPosItem = new MiddleMapPosData(map.Key, subMap.Key, map.Value, decimal.Parse(subMap.Value["width"]), decimal.Parse(subMap.Value["height"]), decimal.Parse(subMap.Value["scale"]), decimal.Parse(subMap.Value["startx"]), decimal.Parse(subMap.Value["starty"]));
                        middleMapInfoMaster.Add((map.Key, subMap.Key), mapPosItem);
                    }
                }
            }
        }

        public static MiddleMapPosData Get(int mapId, int subMapID = 0)
        {
            if (middleMapInfoMaster.ContainsKey((mapId, subMapID)))
                return middleMapInfoMaster[(mapId, subMapID)];
            return null;
        }

        public static IEnumerable<MiddleMapPosData> GetAll() => middleMapInfoMaster.Values.AsEnumerable();
    }
}
