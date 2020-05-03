import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np


class Splitter():

    def __init__(self):
        self.root = ET.parse('input/export.xml').getroot()

    def get_step_count(self):
        df = self.xml_to_csv("HKQuantityTypeIdentifierStepCount")
        df = df.groupby('datetime').sum()
        df.to_csv("output/step_count.csv")
        print("step count <- done.")

    def get_heart_rate(self):
        df = self.xml_to_csv("HKQuantityTypeIdentifierHeartRate")
        df = df[df['HKQuantityTypeIdentifierHeartRate'] > 0]
        df = df.groupby('datetime').agg({np.min, np.max})
        df.columns = [
            'HKQuantityTypeIdentifierHeartRateMin',
            'HKQuantityTypeIdentifierHeartRateMax']
        df.to_csv("output/heart_rate.csv")
        print("heart rate <- done.")

    def get_body_mass(self):
        df = self.xml_to_csv("HKQuantityTypeIdentifierBodyMass")
        df = df.groupby('datetime').sum()
        df.to_csv("output/body_mass.csv")
        print("body mass <- done.")

    def get_burned_energy(self):
        df = self.xml_to_csv("HKQuantityTypeIdentifierBasalEnergyBurned")
        df = df.groupby('datetime').sum()
        df.to_csv("output/burned_energy.csv")
        print("burned energy <- done.")

    def get_walking_distance(self):
        df = self.xml_to_csv("HKQuantityTypeIdentifierDistanceWalkingRunning")
        df = df.groupby('datetime').sum()
        df.to_csv("output/warking_distance.csv")
        print("distance <- done.")

    def get_stand_time(self):
        df = self.xml_to_csv("HKQuantityTypeIdentifierAppleStandTime")
        df = df.groupby('datetime').sum()
        df.to_csv("output/stand_time.csv")
        print("standtime <- done.")

    def xml_to_csv(self, type):
        datetime, counts = [], []

        for child in self.root:
            data = child.attrib

            try:
                if data['type'] == type:
                    datetime.append(data['startDate'])
                    counts.append(data['value'])
            except Exception:
                pass

        df = pd.DataFrame({type: counts})

        df.index = pd.to_datetime(datetime, utc=True)
        df['datetime'] = df.index.tz_convert('Asia/Tokyo')
        df['datetime'] = df.datetime.dt.date
        df[type] = df[type].astype(float)

        return df
