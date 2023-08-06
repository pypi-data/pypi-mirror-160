#!/usr/local/env python3
from .configer import (CalculatePrime, EndlessConfig, GostConfig,
                       StatusMonitorConfig, QbittorrentConfig, SystemConfig,
                       Shadowsocks)
from .installer import AutoRemove, CoreAppInstaller, StatAppInstaller
from .piper import DependencyDownloader


def main():
    exec_classes = [
        SystemConfig, CoreAppInstaller, StatAppInstaller, AutoRemove,
        EndlessConfig, StatusMonitorConfig, GostConfig,
        CalculatePrime, DependencyDownloader, Shadowsocks
    ]
    for ec in exec_classes:
        ec().run()


if __name__ == '__main__':
    main()
