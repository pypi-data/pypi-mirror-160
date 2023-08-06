#      A python library for getting Load Shedding schedules.
#      Copyright (C) 2021  Werner Pieterson
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import List, Tuple

from load_shedding.providers.eskom import Eskom
from load_shedding.libs import coct
from load_shedding.providers import eskom, ProviderError, to_utc
from load_shedding.providers import Province, Stage, Area


class Area(Area):
    def __init__(self, /, **kwargs) -> object:
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.municipality = kwargs.get("municipality")
        self.province = kwargs.get("province")


class CoCT(eskom.Eskom):
    name = "City of Cape Town"

    def get_areas(self, search_text: str = None, max_results: int = None) -> List[Area]:
        try:
            areas: List[Area] = []
            for a in coct.Area:
                area = Area(
                    id=a.value,
                    name=str(a),
                    municipality="City of Cape Town",
                    province=Province.WESTERN_CAPE,
                )
                areas.append(area)
        except Exception as e:
            raise ProviderError(e)
        else:
            return areas

    def get_area_schedule(self, area: Area, stage: Stage) -> List[Tuple]:
        try:
            area_schedule = coct.get_schedule(coct.Area(area.id), stage)
        except Exception as e:
            raise ProviderError(e)
        else:
            area_schedule = to_utc(area_schedule)
            return area_schedule

    def get_stage(self) -> Stage:
        """ Get Stage from Eskom API since we don't have one for CoCT yet."""
        try:
            provider = Eskom()
            stage = provider.get_stage()
        except Exception as e:
            raise ProviderError(e)
        else:
            return stage

