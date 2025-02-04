import React from 'react';

import { Icon } from 'components/kit';
import { Box, Text } from 'components/kit_v2';
import { IconName } from 'components/kit/Icon';

import { RouteStatusEnum } from 'routes/routes';

import { ExplorerCardBadge, ExplorerCardContainer } from './ExplorerCard.style';
import { IExplorerCardProps } from './ExplorerCard.d';

/**
 * @description ExplorerCard component
 * @returns {React.FunctionComponentElement<React.ReactNode>}
 */
function ExplorerCard({
  displayName,
  icon,
  count,
  color,
  description,
  path,
  status,
  isLoading,
}: IExplorerCardProps): React.FunctionComponentElement<React.ReactNode> {
  return (
    <ExplorerCardContainer
      to={path}
      css={{
        backgroundColor: `${color}10`,
        '&:hover': { bs: `0 0 0 1px inset $colors${color}100` },
      }}
    >
      {status && (
        <ExplorerCardBadge
          css={
            status === RouteStatusEnum.NEW
              ? { backgroundColor: '$primary100', color: '#fff' }
              : {}
          }
          weight='$3'
          size='8px'
        >
          {status === RouteStatusEnum.COMING_SOON
            ? 'Explorer coming soon'
            : 'New'}
        </ExplorerCardBadge>
      )}
      <Box display='flex' ai='center' mb='$5'>
        {icon && (
          <Box
            display='flex'
            ai='center'
            jc='center'
            css={{ size: '$7', br: '$pill', background: `${color}100` }}
          >
            <Icon color='white' name={icon as IconName} />
          </Box>
        )}
        <Text css={{ ml: '$5' }} size='$5' weight='$3'>
          {displayName} {isLoading ? null : count ? `(${count})` : null}
        </Text>
      </Box>
      <Text as='p'>{description || ''}</Text>
    </ExplorerCardContainer>
  );
}

export default React.memo(ExplorerCard);
