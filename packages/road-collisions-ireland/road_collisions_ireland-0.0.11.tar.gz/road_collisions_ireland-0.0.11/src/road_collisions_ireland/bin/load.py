from road_collisions_base import logger

from road_collisions_ireland.models.collision import Collisions


def main():
    collisions = Collisions.load_all()

    logger.info('Loaded %s collisions', (len(collisions)))
    logger.info('Do something with the data in the variable \'collisions\'...')

    import pdb; pdb.set_trace()

    pass


if __name__ == '__main__':
    main()
